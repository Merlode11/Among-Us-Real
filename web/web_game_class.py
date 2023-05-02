import os
from threading import Thread
from tkinter import *
from tkinter import messagebox

import pyqrcode
from flask import Flask, render_template, session, redirect, request, Markup

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
                elif self.end:
                    return "/end"
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
            return f'This page does not exist <a href="{where_redirect(session)}">Go home</a>', 404

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
            popup = {"title": Markup(joueur.popup["title"]), "message": Markup(joueur.popup["message"])} \
                if joueur.popup is not None else None
            sound = joueur.popup.get("sound") if joueur.popup is not None else None
            joueur.popup = None

            return render_template(
                "joueur.html",
                code_joueur=str(joueur.id),
                task_list=enumerate(joueur.tasks),
                player=joueur, popup=popup,
                player_role=self.config["names"][joueur.role],
                is_max_asks=joueur.asks >= self.config["max_dead_check"],
                sound=sound
            )
        @app.route("/loading", methods=["GET", "POST"])
        def loading():
            if request.method == "POST" and not session.get("player_id"):
                if self.import_window is None:
                    return redirect("/")
                couleur_joueur = request.form["color"]
                pseudo_joueur = request.form["nickname"]
                ip_joueur = request.remote_addr
                joueur = WebPlayer(ip_joueur, pseudo_joueur, couleur_joueur, self.used_passwords, self.used_id)
                self.players.append(joueur)
                session["player_id"]: int = joueur.id

                # # TODO: Remove the generation of fake players used for testing
                # self.players.extend([
                #     WebPlayer("92.168.0.22", "Joueur 1", "#FF0000", self.used_passwords, self.used_id),
                #     WebPlayer("92.168.0.22", "Joueur 2", "#FF0000", self.used_passwords, self.used_id),
                #     WebPlayer("92.168.0.22", "Joueur 3", "#FF0000", self.used_passwords, self.used_id),
                # ])

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
            popup = {"title": Markup(player.popup["title"]), "message": Markup(player.popup["message"])} \
                if player.popup is not None else None
            sound = player.popup.get("sound") if player.popup is not None else None
            if self.meeting == "coming":
                sound = "emergency_meeting.mp3"
            player.popup = None
            return render_template("meeting.html", players=self.players, player=player, popup=popup, state=self.meeting,
                                   password=player.password, has_voted=player.id in self.meeting_votes.keys(),
                                   sound=sound)

        @app.route("/paused")
        def paused():
            redirection = where_redirect(session)
            if redirection != "/paused":
                return redirect(redirection)
            return render_template("paused.html", message=self.pause_reason)

        @app.route("/end")
        def end():
            redirection = where_redirect(session)
            if redirection != "/end":
                return redirect(redirection)
            del session["player_id"]
            return render_template("end.html")

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
                "role": self.config["names"][player.role],
                "tasks": [task.to_dict() for task in player.tasks],
                "dead": player.dead,
                "asks": player.asks,
                "popup": player.popup,
                "meeting": self.meeting,
                "in_meeting": player in self.meeting_here_users,
                "has_voted": player.id in self.meeting_votes.keys(),
                "game_pause": self.pause,
                "end": self.end
            }
            player.last_message = int(datetime.datetime.now().timestamp())
            for joueur in self.players:
                if joueur.last_message and joueur.last_message + self.config["min_before_inactiv_warn"] * 60 < int(
                        datetime.datetime.now().timestamp()):
                    if player.last_warning and player.last_warning + self.config["min_before_inactiv_kick"] * 60 < int(
                            datetime.datetime.now().timestamp()):
                        if player.warnings >= self.config["max_warns"]:
                            self.send_info_all(
                                f"{player.name} {player.lastname} n'a pas donné de ses nouvelles depuis "
                                f"{self.config['min_before_inactiv_warn'] * player.warnings} minutes. "
                                f"Le jeu est donc en pause le temps qu'on retrouve le joueur")
                            self.pause = True
                            if self.game_master:
                                messagebox.showerror("Un joueur ne répond pas",
                                                     f"{player.name} {player.lastname} n'a pas donné de ses nouvelles d"
                                                     f"epuis {self.config['min_before_inactiv_warn'] * player.warnings}"
                                                     f" minutes. Le jeu est donc en pause le temps qu'on retrouve le joueur."
                                                     f" Un message a été envoyé à tout le monde.")
                    else:
                        player.warnings += 1
                        player.last_warning = int(datetime.datetime.now().timestamp())
                player.popup = None
            return data

        @app.post("/api/kill")
        def kill():
            """
            Kill the player given in the request
            """
            killer = self.get_player(session.get("player_id"))
            if killer is None:
                return {"error": "Joueur assassin introuvable", "error_code": "executor_not_found"}
            killed = self.get_player(request.form["killed_id"])
            if killed is None:
                self.send_info(killer, {"title": "Erreur", "message":
                    "Le joueur que vous souhaitez assassiner n'a pas été trouvé, merci de bien vouloir réessayer."})
                return redirect("/player")
            if killer.role != "impostor":
                self.send_info(killer, {"title": "Erreur", "message":
                    "Vous n'êtes pas un imposteur, vous ne pouvez donc pas assassiner de joueur."})
                return redirect("/player")
            if killed.dead:
                self.send_info(killer,
                               {"title": "Erreur", "message": "Le joueur que vous souhaitez assassiner est déjà mort."})
                return redirect("/player")
            if killed.role == "impostor":
                self.send_info(killer, {"title": "Erreur",
                                        "message": "Vous ne pouvez pas assassiner un autre " + self.config["names"][
                                            "impostor"] + " !"})
                return redirect("/player")
            self.kill_player(killed)
            self.send_info(killed, {
                "title": "Vous êtes mort",
                "message": "Vous avez été assassiné par " + killer.get_name() + ".",
                "sound": "killing.mp3"
            })
            self.send_info(killer, {
                "title": "Joueur assassiné",
                "message": "Vous avez bien assassiné le joueur " + killed.get_name() + ".",
                "sound": "kill.mp3"
            })
            return redirect("/player")

        @app.post("/api/done_task")
        def done_task():
            player = self.get_player(session.get("player_id"))
            task_id = int(request.form.get("task_id"))
            task = player.tasks[task_id]
            if task.done:
                self.send_info(player, {"title": "Erreur", "message": "La tâche a déjà été faite."})
                return redirect("/player")
            if player.role == "impostor":
                self.send_info(player, {"title": "Erreur",
                                        "message": "Vous êtes imposteur, vous ne pouvez pas valider de tâches"})
                return redirect("/player")
            elif "activ" in task.type and not task.active:
                self.send_info(player, {"title": "Erreur",
                                        "message": "La tâche n'a pas été activée. Elle doit-être activée par un mot clé avant de pouvoir la valider."})
                return redirect("/player")
            elif "valid" in task.type:
                if request.form.get("keyword") not in task.keywords:
                    self.send_info(player,
                                   {"title": "Erreur", "message": "Le mot clé pour valider la tâche n'est pas valide."})
                    return redirect("/player")

            self.send_info(player, {
                "title": "Tâche validée",
                "message": "Vous avez bien validé la tâche " + task.name + ".",
                "sound": "task_complete.mp3"
            })
            self.task_done(player, task)
            return redirect("/player")

        @app.post("/api/activ_task")
        def activ_task():
            player = self.get_player(session.get("player_id"))
            task_id = int(request.form.get("task_id"))
            task = player.tasks[task_id]
            if player.role == "impostor":
                self.send_info(player, {"title": "Erreur",
                                        "message": "Vous êtes imposteur, vous ne pouvez pas activer de tâches"})
                return redirect("/player")
            if "activ" not in task.type:
                self.send_info(player, {"title": "Erreur", "message": "La tâche n'est pas activable."})
                return redirect("/player")
            elif task.active:
                self.send_info(player, {"title": "Erreur", "message": "Cette tâche a déjà été activée."})
                return redirect("/player")
            elif request.form.get("keyword") not in task.activ_keywords:
                self.send_info(player,
                               {"title": "Erreur", "message": "Le mot clé pour activer la tâche n'est pas valide."})
                return redirect("/player")
            task.active = True
            self.send_info(player, "Vous avez bien activé la tâche " + task.name + ".")
            return redirect("/player")

        @app.post("/api/report_dead")
        def report_dead():
            player = self.get_player(session.get("player_id"))
            dead_player = self.get_player(request.form["dead_player_id"])
            if dead_player is None:
                self.send_info(player, {"title": "Erreur",
                                        "message": "Le joueur mort n'a pas été trouvé, merci de bien vouloir réessayer avec un identifiant correct."})
                return redirect("/player")
            if player.dead:
                self.send_info(player, {"title": "Erreur",
                                        "message": "Vous êtes mort, vous ne pouvez donc pas signaler un joueur comme mort."})
                return redirect("/player")
            if not dead_player.dead:
                self.send_info(player, {"title": "Erreur",
                                        "message": "Le joueur que vous souhaitez déclarer mort n'est pas mort."})
                return redirect("/player")
            if self.game_master:
                response = messagebox.askokcancel("Mort détecté",
                                                  f"{player.get_name()} découvert un corps ! Il a découvert {dead_player.get_name()}.\n Voulez-vous lancer une réunion ?")
                if response == "ok":
                    self.start_meeting(f"Un cadavre a été signalé par {player.get_name()}.")
                elif response == "cancel":
                    self.send_info(player, "Votre demande a été refusée par l'organisateur.ice de la partie.")
            self.send_info(player, "Vous avez bien signalé le joueur " + dead_player.get_name() + " comme mort.")
            self.start_meeting("Un cadavre a été signalé.")
            return redirect("/player")

        @app.get("/api/see_deads")
        def see_deads():
            player = self.get_player(session.get("player_id"))
            if player is None:
                return {"error": "Joueur non trouvé", "error_code": "player_not_found"}, 400
            if player.role != "scientist":
                self.send_info(player,
                               "Vous n'avez pas le droit de voir les morts. Seul les scientifiques peuvent le faire.")
                return redirect("/player")
            if player.asks >= self.config["max_dead_check"]:
                self.send_info(player, "Vous avez déjà vu les morts trop de fois.")
                return redirect("/player")
            player_status: str = ""
            for joueur in self.players:
                player_status += f'<span style="color: {joueur.color}">{joueur.get_name()}</span> : {"mort" if joueur.dead else "vivant"}<br>'
            self.send_info(player, player_status)
            player.asks += 1
            return redirect("/player")

        @app.get("/api/game_is_started")
        def game_is_started():
            return {"started": self.import_window is None}, 200

        @app.post("/api/vote")
        def vote():
            player = self.get_player(session.get("player_id"))
            if player is None:
                return {"error": "Joueur non trouvé", "error_code": "player_not_found"}, 400
            if player.dead:
                self.send_info(player, "Vous êtes mort, vous ne pouvez donc pas voter.")
                return redirect("/meeting")
            player_id = request.form["vote"]
            voted_player = self.get_player(player_id) if player_id != "skip" else None
            if voted_player is None and player_id != "skip":
                self.send_info(player,
                               "Le joueur que vous souhaitez voter n'a pas été trouvé, merci de bien vouloir réessayer avec un identifiant correct.")
                return redirect("/meeting")
            if player.id in self.meeting_votes.keys():
                self.send_info(player, "Vous avez déjà voté.")
                return redirect("/meeting")
            player.voted = True
            self.meeting_votes[player.id] = player_id if voted_player is not None else "skip"
            print(self.meeting_votes)
            self.send_info(player, {
                "title": "Vote enregistré",
                "message": "Vous avez bien voté pour " + (
                    voted_player.get_name() if voted_player is not None else "passer"),
                "sound": "avote.mp3"
            })
            return redirect("/meeting")

        @app.get("/api/sos")
        def sos():
            player = self.get_player(session.get("player_id"))
            if player is None:
                return {"error": "Joueur non trouvé", "error_code": "player_not_found"}, 400
            message = request.form.get("message")
            self.pause = True
            self.pause_reason = message if message else "Aide demandé par " + player.get_name()
            code = self.set_pause_game()
            self.send_info(player, {"title": "Demande envoyée",
                                    "message": f"Votre demande d'aide a bien été envoyée. Votre code pour annuler l'urgence est {code}"})
            return redirect("/player")

        self.flt = flt = Thread(target=lambda: app.run(host="0.0.0.0", port=80, debug=False))
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
        else:
            self.players = [None] * 100
            self.import_window = popup = Tk()
            popup.title("Importation des joueurs")
            popup.geometry("300x200")
            popup.resizable(True, True)
            popup.iconbitmap(self.path + "/assets/img/amongus.ico")
            popup.state("zoomed")
            game_qrcode = pyqrcode.create(f"http://{self.ip}:80/")
            game_qrcode.png(self.path + "/assets/img/qrcode.png", scale=6)

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

        popup.protocol("WM_DELETE_WINDOW", closing)

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
            new_message = new_message.replace("{lastname}", player.get_name())
            new_message = new_message.replace("{role}", self.config["names"][player.role])
            new_message = new_message.replace("{id}", player.id)
            new_message = new_message.replace("{phone}", player.ip)
            new_message = new_message.replace("{tasks}", "\n".join([task.name for task in player.tasks]))
            new_message = new_message.replace("{password}", player.password)

            print(player.get_name(), ":", new_message)
            player.popup = {"title": "Information", "message": new_message}

    def send_info(self, player: WebPlayer, dictionnaire: dict or str = {"title": "Information", "message": ""}):
        if isinstance(dictionnaire, str):
            dictionnaire = {"title": "Information", "message": dictionnaire}
        print(player.nickname, ":", dictionnaire["message"])
        dictionnaire["message"] = dictionnaire["message"].replace("\n", "<br/>")
        player.popup = dictionnaire

    def send_role(self, player) -> None:
        """
        Envoie un message au joueur indiquant son role et ses tâches
        :param player: WebPlayer: Le joueur avec son numéro de téléphone
        """
        message = f"Bonjour {player.get_name()},<br/>"
        message += "Vous êtes un " + self.config["names"][player.role].upper()
        if player.role == "impostor":
            impostors = " ".join([(joueur.get_name()) for joueur in self.impostors])
            message += " avec " + impostors + "<br/><br/>"
        else:
            message += "<br/><br/>"
        message += "Vos tâches sont:<br/>"
        for i in range(len(player.tasks)):
            task = player.tasks[i]
            message += f"{i + 1}: {task.name} ({task.steps} étapes)<br/>"
        message += "<br/>"
        message += f"Votre identifiant est {player.id}<br/>"
        message += "<br/>"
        message += "Nous vous souhaitons une bonne partie !"

        self.send_info(player, message)

    def end_game(self):
        """
        Termine la partie
        :return:
        """
        self.window.destroy()
        self.flt.join()
        exit(0)


if __name__ == '__main__':
    game = WebGame()
