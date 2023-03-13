from flask import Flask, render_template, session
from game_class import Game
from classes import WebPlayer
import os
from threading import Timer
from tkinter import Tk, Label, Button, Entry, StringVar, messagebox
from utils import clear_frame

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
        - POST /api/kill/killer_id/killed_id: Permet pour le tueur de tuer une personne
        - POST /api/done_task/player_id/task_id: Permet de valider une tâche comme faite
        - POST /api/activ_task/player_id/task_id: Permet d'activer une tâche du joueur
    """
    def __init__(self, game_master: bool = None):
        self.server = app = Flask(__name__)
        self.receive = False
        self.game_master = game_master
        self.config = None

        app.secret_key = os.urandom(24) # It's for the session system of flask

        @app.errorhandler(404)
        def page_not_found(error):
            return 'This page does not exist', 404

        @app.route("/")
        def index():
            return render_template("home.html")

        @app.route("/joueur", methods=["GET", "POST"])
        def joueur_page():
            if request.method == "POST":
                # Get the passed informations in the json request
                couleur_joueur = request.form["color"]
                pseudo_joueur = request.form["nickname"]
                ip_joueur = request.remote_addr
                joueur = WebPlayer(ip_joueur, pseudo_joueur, couleur_joueur, [])

            return render_template("joueur.html", code_joueur="123456789", task_list=["tache1", "tache2", "tache3"])
            
        @app.route("/loading")
        def loading(): 
            return render_template("loading.html")
        
        @app.route("/meeting")
        def meeting(): 
            return render_template("meeting.html", players=self.players)
        
        @app.route("/paused")
        def paused(): 
            return render_template("paused.html", game={"paused": self.pause, "message": self.pause_reason})

        @app.get("/api/infos/<code_joueur>")
        def infos(code_joueur):
            """
            Returns a json with the information of the player
            :param code_joueur:
            :return:
            """
            player = self.get_player(code_joueur)
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
        
        @app.post("/api/kill/<path:killer_path>")
        def kill(killer_path):
            """
            Kill the player given in thz request
            """
            killer_id, killed_id = killer_path.split("/")
            killer = self.get_player(killer_id)
            if killer is None:
                return {"error": "Joueur assassin introuvable", "error_code": "executor_not_found"}
            killed = self.get_player(killed_id)
            if killed is None:
                return {"error": "Joueur assassiné introuvable", "error_code": "target_not_found"}
            if killer.role != "impostor": 
                return {"error": "Joueur n'étant pas imposteur", "error_code": "not_impostor"}
            if killed.dead:
                return {"error": "Joueur assassiné déjà mort", "error_code": "target_dead"}
            self.kill_player(killed)
            return {"success": True}, 200
        
        @app.post("/api/done_task/<path:task_path>")
        def done_task(task_path):
            player_id, task_id = task_path.split("/")
            # TODO: Chercher pour avoir les informations de la requête (si jamais un mot a été fourni)
            player = self.get_player(player_id)
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
        
        @app.post("/api/activ_task/<path:task_path>")
        def activ_task(task_path):
            player_id, task_id = task_path.split("/")
            player = self.get_player(player_id)
            task = player.tasks[task_id]
            if "activ" not in task.type:
                return {"error": "Le type de tâche n'est pas correct", "error_code": "invalid_task_type"}
            elif task.active:
                return {"error": "La tâche est déjà active", "error_code": "task_active"}
            elif request.body["keyword"] not in task.activ_keywords:
                return {"error": "Ce mot n'est pas valide", "error_code": "unknown_keyword"}
            task.active = True

        Timer(1, super().__init__, args=(game_master,)).start()
        app.run(host="0.0.0.0", port=80, debug=True)


    def import_players(self):
        """
        Créé une fenêtre Tkinter popup pour attendre que les joueurs se connectent
        :return:
        """
        
        if self.import_window:
            clear_frame()
            return None
        
        self.players = [None] * 100
        self.import_window = popup = Tk()
        popup.title("Importation des joueurs")
        popup.geometry("300x200")
        popup.resizable(True, True)
        popup.iconbitmap(self.path + "/assets/img/amongus.ico")
        popup.configure(bg="#2c2f33")
        
        main_frame = Frame(popup)
        
        start_button = Button(main_frame)
        
        self.import_players_frame = VerticalScrolledFrame(popup)
        



    def send_info_all(self, message: str):
        for player in self.players:
            # replace the variable in the message
            new_message = message.replace("{name}", player.name)
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
