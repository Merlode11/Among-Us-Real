import json
import os
from threading import Thread
from tkinter import *
from tkinter import messagebox

import pyqrcode
from flask import Flask, render_template, session, redirect, request

from classes import WebPlayer
from game_class import Game
from utils import clear_frame, VerticalScrolledFrame
import datetime
import socket


class WebGame(Game):
    """
    Initialise une partie de jeu en utilisant le mode de jeu web.
    
    Liste des requêtes API:
        - GET /: Affiche la page principale
        - GET /joueur: Affiche la page du joueur
        - POST /joueur: Enregistre un joueur dans la partie
        - GET /meeting: Affiche la page de réunion du joueur
        - GET /paused: Affiche la page de pause de jeu en cas d'urgence
        - GET /api/infos/<code_joueur>: Renvoie les informations actuelles du joueur
        - POST /api/kill: Permet pour le tueur de tuer une personne
        - POST /api/done_task/task_id: Permet de valider une tâche comme faite
        - POST /api/activ_task/task_id: Permet d'activer une tâche du joueur
    """

    def __init__(self, game_master: bool = None):
        self.import_players_frame = None
        self.server = app = Flask(__name__)
        self.receive: bool = False
        self.game_master: bool = game_master
        self.config: dict or None = None
        self.import_window: Tk or None = None
        self.players: list[WebPlayer] = []
        self.used_passwords: list[str] = []
        self.used_id: list[int] = []
        self.ip: str = socket.gethostbyname(socket.gethostname())

        app.secret_key = os.urandom(24)  # It's for the session system of flask

        def where_redirect(sess) -> str:
            if sess.get("player_id"):
                if self.import_window is not None:
                    return "/loading"
                elif self.meeting:
                    return "/meeting"
                elif self.pause:
                    return "/paused"
                else:
                    return "/player"
            else:
                return "/"

        @app.errorhandler(404)
        def page_not_found(error):
            return 'This page does not exist <a href="/">Go home</a>', 404

        @app.route("/")
        def index():
            redirection = where_redirect(session)
            if redirection != "/":
                return redirect(redirection)
            return render_template("home.html")

        @app.route("/player")
        def joueur_page():
            player_id = session.get("player_id")
            redirection = where_redirect(session)
            if redirection != "/player":
                return redirect(redirection)
            joueur = self.get_player(player_id)
            return render_template("joueur.html", code_joueur=str(joueur.id), task_list=joueur.tasks, player=joueur)

        @app.route("/loading", methods=["GET", "POST"])
        def loading():
            if request.method == "POST":
                couleur_joueur = request.form["color"]
                pseudo_joueur = request.form["nickname"]
                ip_joueur = request.remote_addr
                joueur = WebPlayer(ip_joueur, pseudo_joueur, couleur_joueur, self.used_passwords, self.used_id)
                self.players.append(joueur)
                session["player_id"]: int = joueur.id
                self.import_players()
            elif request.method == "GET":
                redirection = where_redirect(session)
                if redirection != "/loading":
                    return redirect(redirection)
            return render_template("loading.html")

        @app.route("/meeting")
        def meeting():
            player_id = session.get("player_id")
            player = self.get_player(player_id)
            redirection = where_redirect(session)
            if redirection != "/meeting":
                return redirect(redirection)
            return render_template("meeting.html", players=self.players, player=player, game=self)

        @app.route("/paused")
        def paused():
            redirection = where_redirect(session)
            if redirection != "/paused":
                return redirect(redirection)
            return render_template("paused.html", message=self.pause_reason)

        @app.get("/api/infos/")
        def infos():
            """
            Returns a json with the information of the player
            :return:
            """
            player = self.get_player(session.get("player_id"))
            if player is None:
                return {"error": "Joueur introuvable", "error_code": "executor_not_found"}
            data = {
                "ip": player.ip,
                "nickname": player.nickname,
                "color": player.color,
                "id": player.id,
                "password": player.password,
                "role": player.role,
                "tasks": player.tasks,
                "dead": player.dead,
                "asks": player.asks,
                "popup": player.popup,
                "meeting": self.meeting,
                "in_meeting": player in self.meeting_here_users,
                "game_pause": game.pause
            }
            player.popup = None
            player.last_message = int(datetime.datetime.now().timestamp())
            return data

        @app.post("/api/kill/")
        def kill():
            """
            Kill the player given in the request
            """
            killer = self.get_player(session.get("player_id"))
            if killer is None:
                return {"error": "Joueur assassin introuvable", "error_code": "executor_not_found"}
            killed = self.get_player(request.form["killed_id"])
            if killed is None:
                return render_template(
                    "joueur.html",
                    code_joueur=str(killer.id),
                    task_list=killer.tasks,
                    player=killer,
                    popup={"title": "Erreur",
                           "message": "Le joueur que vous souhaitez assassiner n'a pas été trouvé, merci de bien vouloir réessayer."}
                ), 400
            if killer.role != "impostor":
                return render_template(
                    "joueur.html",
                    code_joueur=str(killer.id),
                    task_list=killer.tasks,
                    player=killer,
                    popup={"title": "Erreur",
                           "message": "Vous n'êtes pas imposteur, vous ne pouvez pas assassiner de joueur."}
                ), 400
            if killed.dead:
                return render_template(
                    "joueur.html",
                    code_joueur=str(killer.id),
                    task_list=killer.tasks,
                    player=killer,
                    popup={"title": "Erreur", "message": "Le joueur que vous souhaitez assassiner est déjà mort."}
                ), 400
            self.kill_player(killed)
            return render_template(
                "joueur.html",
                code_joueur=str(killer.id),
                task_list=killer.tasks,
                player=killer,
                popup={"title": "Joueur assasiné",
                       "message": "Vous avez bien assassiné le joueur " + killed.get_name() + "."}
            ), 200

        @app.post("/api/done_task/<int:task_id>")
        def done_task(task_id):
            player = self.get_player(session.get("player_id"))
            task = player.tasks[task_id]
            if task.done:
                return render_template(
                    "joueur.html",
                    code_joueur=str(player.id),
                    task_list=player.tasks,
                    player=player,
                    popup={"title": "Erreur", "message": "La tâche a déjà été faite."}
                ), 400
            elif "activ" in task.type and not task.active:
                return render_template(
                    "joueur.html",
                    code_joueur=str(player.id),
                    task_list=player.tasks,
                    player=player,
                    popup={"title": "Erreur",
                           "message": "La tâche n'a pas été activée. Elle doit-être activée par un mot clé avant de piuvoir la validée."}
                ), 400
            elif "valid" in task.type:
                if request.form["keyword"] not in task.keywords:
                    return render_template(
                        "joueur.html",
                        code_joueur=str(player.id),
                        task_list=player.tasks,
                        player=player,
                        popup={"title": "Erreur", "message": "Le mot clé pour valider la tâche n'est pas valide."}
                    ), 400
            self.task_done(player, task)
            return render_template(
                "joueur.html",
                code_joueur=str(player.id),
                task_list=player.tasks,
                player=player,
                popup={"title": "Tâche validée", "message": "Vous avez bien validé la tâche " + task.name + "."}
            ), 200

        @app.post("/api/activ_task/<int:task_id>")
        def activ_task(task_id):
            player = self.get_player(session.get("player_id"))
            task = player.tasks[task_id]
            if "activ" not in task.type:
                return render_template(
                    "joueur.html",
                    code_joueur=str(player.id),
                    task_list=player.tasks,
                    player=player,
                    popup={"title": "Erreur", "message": "La tâche n'est pas une tâche activable."}
                ), 400
            elif task.active:
                return render_template(
                    "joueur.html",
                    code_joueur=str(player.id),
                    task_list=player.tasks,
                    player=player,
                    popup={"title": "Erreur", "message": "La tâche a déjà été activée."}
                ), 400
            elif request.form["keyword"] not in task.activ_keywords:
                return render_template(
                    "joueur.html",
                    code_joueur=str(player.id),
                    task_list=player.tasks,
                    player=player,
                    popup={"title": "Erreur", "message": "Le mot clé pour activer la tâche n'est pas valide."}
                ), 400
            task.active = True
            return render_template(
                "joueur.html",
                code_joueur=str(player.id),
                task_list=player.tasks,
                player=player,
                popup={"title": "Tâche activée", "message": "Vous avez bien activé la tâche " + task.name + "."}
            ), 200

        @app.post("/api/report_dead")
        def report_dead():
            player = self.get_player(session.get("player_id"))
            dead_player = self.get_player(request.form["dead_player_id"])
            if dead_player is None:
                return render_template(
                    "joueur.html",
                    code_joueur=str(player.id),
                    task_list=player.tasks,
                    player=player,
                    popup={"title": "Erreur",
                           "message": "Le joueur mort n'a pas été trouvé, merci de bien vouloir réessayer avec un identifiant correct."}
                ), 400
            if not dead_player.dead:
                return render_template(
                    "joueur.html",
                    code_joueur=str(player.id),
                    task_list=player.tasks,
                    player=player,
                    popup={"title": "Erreur", "message": "Le joueur que vous souhaitez déclarer mort n'est pas mort."}
                ), 400
            if self.game_master:
                response = messagebox.askokcancel("Mort détecté",
                                                  f"{player.name} {player.lastname} découvert un corps ! Il a découvert {dead_player.get_name()}.\n Voulez-vous lancer une réunion ?")
                if response == "ok":
                    game.start_meeting(f"Un cadavre a été signalé par {player.get_name()}.")
                elif response == "cancel":
                    self.send_info(player, "Votre demande a été refusée par l'organisateur.ice de la partie.")
            self.start_meeting("Un cadavre a été signalé.")
            return render_template(
                "joueur.html",
                code_joueur=str(player.id),
                task_list=player.tasks,
                player=player,
                popup={"title": "Joueur signalé",
                       "message": "Vous avez bien signalé le joueur " + dead_player.get_name() + " comme mort."}
            ), 200

        @app.post("/api/see_deads")
        def see_deads():
            player = self.get_player(session.get("player_id"))
            if player is None:
                return {"error": "Joueur non trouvé", "error_code": "player_not_found"}, 400
            if player.role != "scientist":
                return render_template(
                    "joueur.html",
                    code_joueur=str(player.id),
                    task_list=player.tasks,
                    player=player,
                    popup={"title": "Erreur",
                           "message": "Vous n'avez pas le droit de voir les morts. Seul les scientifiques peuvent le faire."}
                ), 400
            if player.asks >= self.config["max_dead_check"]:
                return render_template(
                    "joueur.html",
                    code_joueur=str(player.id),
                    task_list=player.tasks,
                    player=player,
                    popup={"title": "Erreur", "message": "Vous avez déjà vu les morts trop de fois."}
                ), 400
            player_status: str = ""
            for joueur in self.players:
                player_status += f'<span style="color: {joueur.color}">{joueur.get_name()}</span> : {"mort" if joueur.dead else "vivant"}<br>'
            return render_template(
                "joueur.html",
                code_joueur=str(player.id),
                task_list=player.tasks,
                player=player,
                popup={"title": "Voici l'état de chaque joueur actuellement", "message": player_status}
            ), 200

        @app.get("/api/game_is_started")
        def game_is_started():
            return self.import_window is not None, 200

        @app.post("/api/vote")
        def vote():
            player = self.get_player(session.get("player_id"))
            if player is None:
                return {"error": "Joueur non trouvé", "error_code": "player_not_found"}, 400
            voted_player = self.get_player(request.form["voted_player_id"])
            if voted_player is None:
                return render_template(
                    "meeting.html",
                    players=self.players,
                    player=player,
                    popup={"title": "Erreur", "message": "Le joueur que vous souhaitez voter n'a pas été trouvé."},
                    game=self
                ), 400
            if player.voted:
                return render_template(
                    "meeting.html",
                    players=self.players,
                    player=player,
                    popup={"title": "Erreur", "message": "Vous avez déjà voté."},
                    game=self
                ), 400
            player.voted = True



        @app.get("/api/sos")
        def sos():
            player = self.get_player(session.get("player_id"))
            if player is None:
                return {"error": "Joueur non trouvé", "error_code": "player_not_found"}, 400
            if player.role != "doctor":
                return {"error": "Vous n'êtes pas le docteur", "error_code": "not_doctor"}, 400
            if player.sos_used:
                return {"error": "Vous avez déjà utilisé votre SOS", "error_code": "sos_already_used"}, 400
            player.sos_used = True
            player.sos_used_in = self.meeting
            return {"message": "Vous avez bien utilisé votre SOS"}, 200

        flt = Thread(target=lambda: app.run(host="0.0.0.0", port=80, debug=False))
        flt.daemon = True
        flt.start()
        super().__init__()

    def import_players(self):
        """
        Créé une fenêtre Tkinter popup pour attendre que les joueurs se connectent
        :return:
        """
        already_started: bool = self.import_window is not None
        if self.import_window:
            clear_frame(self.import_window)
            popup = self.import_window
            game_qrcode = pyqrcode.create(f"http://{self.ip}:80/")
            game_qrcode.png(self.path + "/assets/img/qrcode.png", scale=6)
        else:
            self.players = [None] * 100
            self.import_window = popup = Tk()
            popup.title("Importation des joueurs")
            popup.geometry("300x200")
            popup.resizable(True, True)
            popup.iconbitmap(self.path + "/assets/img/amongus.ico")
            popup.state("zoomed")

        def start_game() -> None:
            """
            Démarre la partie, une fois que les joueurs sont importés
            :return: None
            """
            self.import_window = None
            self.players = [player for player in self.players if player is not None]
            popup.destroy()
            self.start_game()
            return None

        def closing():
            """
            Fonction de fermeture de la fenêtre
            """
            if messagebox.askokcancel("Quitter", "Êtes vous sûr de quitter ?"):
                popup.destroy()
                self.window.destroy()

        main_frame = Frame(popup)

        qrcode_frame = Frame(main_frame)

        qrcode = PhotoImage(file=self.path + "/assets/img/qrcode.png", master=qrcode_frame)

        qrcode_label = Label(qrcode_frame, image=qrcode)
        qrcode_label.pack()

        url_label = Label(qrcode_frame, text=f"http://{self.ip}:80/", font=("Arial", 28), fg="blue", cursor="hand2")
        url_label.pack()

        qrcode_frame.pack(fill=BOTH, expand=True)

        valid_players = [player for player in self.players if player is not None]

        start_button = Button(main_frame, text="Démarrer la partie", command=start_game)

        if len(valid_players) < 4:
            start_button.config(state=DISABLED)

        start_button.pack()

        import_players_frame = VerticalScrolledFrame(main_frame)

        for player in valid_players:
            player_frame = Frame(import_players_frame)

            player_label = Label(player_frame, text=player.get_name(), font=("Arial", 28), fg=player.color)
            player_label.pack()

            player_frame.pack(fill=BOTH, expand=True)

        import_players_frame.pack(fill=BOTH, expand=True)

        main_frame.pack(fill=BOTH, expand=True)

        if not already_started:
            popup.mainloop()

    def send_info_all(self, message: str):
        for player in self.players:
            # replace the variable in the message
            new_message = message.replace("{name}", player.nickname)
            new_message = new_message.replace("{lastname}", player.lastname)
            new_message = new_message.replace("{role}", self.config["names"][player.role])
            new_message = new_message.replace("{id}", player.id)
            new_message = new_message.replace("{phone}", player.phone)
            new_message = new_message.replace("{tasks}", "\n".join([task.name for task in player.tasks]))
            new_message = new_message.replace("{password}", player.password)

            print(player.name, ":", new_message)
            player.popup = new_message

    def send_info(self, player: WebPlayer, message: str):
        print(player.nickname, ":", message)
        player.popup = message

    def send_role(self, player) -> None:
        """
        Envoie un message au joueur indiquant son role et ses tâches
        :param player: WebPlayer: Le joueur avec son numéro de téléphone
        """
        message = f"Bonjour {player.name} {player.lastname},\n"
        message += "Vous êtes un " + self.config["names"][player.role].upper()
        if player.role == "impostor":
            impostors = " ".join([(joueur.name + " " + joueur.lastname) for joueur in self.impostors])
            message += " avec " + impostors + "\n\n"
        else:
            message += "\n\n"
        message += "Vos tâches sont:\n"
        for i in range(len(player.tasks)):
            task = player.tasks[i]
            message += f"{i + 1}: {task.name} ({task.classe})\n"
        message += "\n"
        message += f"Votre identifiant est {player.id}\n"
        message += "\n"
        message += "Pour voir toutes les commandes, vous pouvez taper \"help\"\n"
        message += "Nous vous souhaitons une bonne partie !"

        self.send_info(player, message)


if __name__ == '__main__':
    game = WebGame()
