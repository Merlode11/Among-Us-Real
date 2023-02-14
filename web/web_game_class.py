from flask import Flask, render_template
from game_class import Game
from classes import WebPlaye
import json


class WebGame(Game):
    def __init__(self, ip: str, port: int, game_master: bool = None):
        self.ip = ip
        self.port = port
        self.server = app = Flask(__name__)
        self.receive = False
        self.game_master = game_master
        self.config = None

        @app.route("/")
        def index():
            return render_template("home.html")

        @app.route("/joueur")
        def joueur():
            return render_template("joueur.html", code_joueur="123456789", task_list=["tache1", "tache2", "tache3"])

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
                "popup": player.popup
            }
            player.popup = None
            return data
        
        @app.post("/api/kill/<killer_id/<killed_id>")
        def kill(killer_id, killed_id):
            """
            Kill the player given in thz request
            """
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
            return {"success": True}
        
        @app.post("/api/done_task/<player_id>/<task_id>")
        def done_task(player_id, task_id):
            # TODO: Chercher pour avoir les informations de la requête (si jamais un mot a été fourni)
            player = self.get_player(player_id)
            task = player.tasks[task_id]
            if task.done:
                return {"error": "La tâche a déjà été faite", "error_code": "task_already_done"}
            elif "activ" in task.type and not task.active: 
                return {"error": "La tâche n'a pas été activée", "error_code": "task_inactive"}
            elif "valid" in task.type:
                if req.body["keyword"] not in task.keywords: 
                    return {"error": "Ce mot n'est pas valide", "error_code": "unknown_keyword"}
            self.task_done(player, task)
            return {"success": True, "task": task}
        
        @app.post("/api/activ_task/<player_id>/<task_id>")
        def activ_task(player_id, task_id): 
            player = self.get_player(player_id)
            task = player.tasks[task_id]
            if "activ" not in task.type:
                return {"error": "Le type de tâche n'est pas correct", "error_code": "invalid_task_type"}
            elif task.active:
                return {"error": "La tâche est déjà active", "error_code": "task_active"}
            elif req.body["keyword"] not in task.activ_keywords: 
                return {"error": "Ce mot n'est pas valide", "error_code": "unknown_keyword"}
            task.active = True
            

        super().__init__(game_master)

    def import_players(self):
        used_passwords: list = []
        used_id: list = []


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
    SMSGame(True)
