import os
from threading import Thread
from tkinter import *

import pyqrcode
from flask import Flask, render_template, session, url_for, redirect, request

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

        print("http://" + self.ip + ":80")

        @app.errorhandler(404)
        def page_not_found(error):
            return 'This page does not exist <a href="/">Go home</a>', 404

        @app.route("/")
        def index():
            if session.get("player_id"):
                print(session.get("player_id"))
                return redirect(url_for("/player"))
            return render_template("home.html")

        @app.route("/player")
        def joueur_page():
            player_id = session["player_id"]
            if not player_id:
                return redirect(url_for("/"))
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
            return render_template("loading.html")

        @app.route("/meeting")
        def meeting():
            player_id = session["player_id"]
            if not player_id:
                return redirect(url_for("/"))
            return render_template("meeting.html", players=self.players)

        @app.route("/paused")
        def paused():
            player_id = session["player_id"]
            if not player_id:
                return redirect(url_for("/"))
            return render_template("paused.html", game={"paused": self.pause, "message": self.pause_reason})

        @app.get("/api/infos/")
        def infos():
            """
            Returns a json with the information of the player
            :return:
            """
            player = self.get_player(session["player_id"])
            if player is None:
                return {"error": "Joueur introuvable", "error_code": "executor_not_found"}
            data = {
                "ip": player.ip,
                "nickname": player.nickname,
                "color": player.color,
                "id": player.id,
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

            killer = self.get_player(session["player_id"])
            if killer is None:
                return {"error": "Joueur assassin introuvable", "error_code": "executor_not_found"}
            killed = self.get_player(request.form["killed_id"])
            if killed is None:
                return {"error": "Joueur assassiné introuvable", "error_code": "target_not_found"}
            if killer.role != "impostor":
                return {"error": "Joueur n'étant pas imposteur", "error_code": "not_impostor"}
            if killed.dead:
                return {"error": "Joueur assassiné déjà mort", "error_code": "target_dead"}
            self.kill_player(killed)
            return {"success": True}, 200

        @app.post("/api/done_task/<int:task_id>")
        def done_task(task_id):
            # TODO: Chercher pour avoir les informations de la requête (si jamais un mot a été fourni)
            player = self.get_player(session["player_id"])
            task = player.tasks[task_id]
            if task.done:
                return {"error": "La tâche a déjà été faite", "error_code": "task_already_done"}
            elif "activ" in task.type and not task.active:
                return {"error": "La tâche n'a pas été activée", "error_code": "task_inactive"}
            elif "valid" in task.type:
                if request.form["keyword"] not in task.keywords:
                    return {"error": "Ce mot n'est pas valide", "error_code": "unknown_keyword"}
            self.task_done(player, task)
            return {"success": True, "task": task}, 200

        @app.post("/api/activ_task/<int:task_id>")
        def activ_task(task_id):
            player = self.get_player(session["player_id"])
            task = player.tasks[task_id]
            if "activ" not in task.type:
                return {"error": "Le type de tâche n'est pas correct", "error_code": "invalid_task_type"}
            elif task.active:
                return {"error": "La tâche est déjà active", "error_code": "task_active"}
            elif request.form["keyword"] not in task.activ_keywords:
                return {"error": "Ce mot n'est pas valide", "error_code": "unknown_keyword"}
            task.active = True
            return {"success": True, "task": task}, 200

        @app.post("/api/report_dead")
        def report_dead():
            player = self.get_player(session["player_id"])
            dead_player = self.get_player(request.form["dead_player_id"])
            if dead_player is None:
                return {"error": "Joueur assassiné introuvable", "error_code": "target_not_found"}
            if not dead_player.dead:
                return {"error": "Joueur assassiné n'est pas mort", "error_code": "target_not_dead"}
            self.s

        @app.get("/api/game_is_started")
        def game_is_started():
            return self.import_window is not None, 200

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

        main_frame = Frame(popup)

        qrcode_frame = Frame(main_frame)

        qrcode = PhotoImage(file=self.path + "/assets/img/qrcode.png", master=qrcode_frame)

        qrcode_label = Label(qrcode_frame, image=qrcode)
        qrcode_label.pack()

        url_label = Label(qrcode_frame, text=f"http://{self.ip}:80/", font=("Arial", 28), fg="blue", cursor="hand2")
        url_label.pack()

        qrcode_frame.pack(fill=BOTH, expand=True)

        valid_players = [player for player in self.players if player is not None]

        import_players_frame = VerticalScrolledFrame(main_frame)

        for player in valid_players:
            player_frame = Frame(import_players_frame)

            player_label = Label(player_frame, text=player.get_name(), font=("Arial", 28), fg=player.color)
            player_label.pack()

            player_frame.pack(fill=BOTH, expand=True)

        import_players_frame.pack(fill=BOTH, expand=True)

        start_button = Button(main_frame, text="Démarrer la partie", command=start_game)

        if len(valid_players) < 4:
            start_button.config(state=DISABLED)

        start_button.pack()

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
