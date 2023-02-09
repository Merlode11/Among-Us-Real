from flask import Flask, render_template
from game_class import Game
from classes import WebPlayer


class WebGame(Game):
    def __init__(self, ip: str, port: int, game_master: bool = None):
        self.ip = ip
        self.port = port
        self.server = None
        self.receive = False
        self.game_master = game_master
        self.config = None
        app = Flask(__name__)

        @app.route("/")
        def index():
            return render_template("home.html")

        @app.route("/joueur")
        def joueur():
            return render_template("joueur.html", code_joueur="123456789", task_list=["tache1", "tache2", "tache3"])

        @app.get("/infos/<code_joueur>")
        def infos(code_joueur):
            """
            Returns a json with the information of the player
            :param code_joueur:
            :return:
            """
            player = next((joueur for joueur in self.players if joueur.id == code_joueur), None)
            if player is None:
                return {"error": "Joueur introuvable"}
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

        super().__init__(game_master)

    def import_players(self):
        used_passwords: list = []
        used_id: list = []


    def send_info_all(self, message: str):
        for player in self.players:
            new_message = message.replace("{name}", player.name)
            # replace the variable in the message
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

        self.send_messages.append(message)
        self.send_info(player, message)

    def check_command(self, player, message: str) -> bool:
        """
        Vérifie si jamais le message reçu est une commande ou un message validant une tâche. Si c’est le cas, on l'exécute
        :param player: SMSPlayer: Le joueur qui a envoyé le message
        :param message: str: le contenu du message reçu
        :return: bool: Si jamais le message était bien une commande
        """
        message = message.lower()
        for cmd in commands:
            if message.startswith(tuple([cmd.name] + cmd.aliases)):
                return cmd.run(player, message, self)
        for task in player.tasks:
            if task.type == "validate_basic":
                for word in task.keywords:
                    if word in message:
                        self.task_done(player, task)
                        return True
            elif task.type == "activate_basic":
                for word in task.activ_keywords:
                    if word in message:
                        send_sms(player.phone, f"La tâche {task.name} vous envoie:\n{task.message}")
                        task.active = True
                        return True
            elif task.type == "activ_valid":
                for word in task.keywords:
                    if word in message:
                        if task.active:
                            self.task_done(player, task)
                            return True
                        else:
                            send_sms(player.phone, "La tâche n'est pas encore activée")
                            return True
                for word in task.activ_keywords:
                    if word in message:
                        send_sms(player.phone, f"La tâche {task.name} vous envoie:\n{task.message}")
                        task.active = True
                        return True

        return False

    def start_recieve_sms(self):
        """
        Active la vérification périodique de la réception de SMS
        """

        def recieve():
            try:
                new = get_new_messages(self)
            except Exception as e:
                # print(e)
                new = []
            if len(new) > 0:
                for msg in new:
                    if msg.content in self.send_messages:
                        del self.send_messages[self.send_messages.index(msg.content)]
                        continue
                    joueur = next((joueur for joueur in self.players if joueur.phone == msg.phone), None)
                    if self.check_command(joueur, msg.content):
                        continue
                    string = "Nouveau message de " + joueur.name + " " + joueur.lastname + " (" + joueur.phone + ") :\n"
                    string += msg.content
                    messagebox.showinfo(f"Message de {msg.phone}", string)

            for player in self.players:
                if player.last_message and player.last_message + self.config["min_before_inactiv_warn"] * 60 < int(
                        datetime.datetime.now().timestamp()):
                    if player.last_warning and player.last_warning + self.config["min_before_inactiv_kick"] * 60 < int(
                            datetime.datetime.now().timestamp()):
                        if player.warnings >= self.config["max_warns"]:
                            self.send_info_all(
                                f"{player.name} {player.lastname} n'a pas donné de ses nouvelles depuis {self.config['min_before_inactiv_warn'] * player.warnings} minutes. Le jeu est donc en pause le temps qu'on retrouve le joueur")
                            self.pause = True
                            if self.game_master:
                                messagebox.showerror("Un joueur ne répond pas",
                                                     f"{player.name} {player.lastname} n'a pas donné de ses nouvelles depuis {self.config['min_before_inactiv_warn'] * player.warnings} minutes. Le jeu est donc en pause le temps qu'on retrouve le joueur. Un message a été envoyé à tout le monde.")
                        else:
                            send_sms(player.phone,
                                     f"Il y a un problème ? Nous n'avons pas reçu de message depuis {self.config['min_before_inactiv_warn'] * player.warnings} minutes. Si tout va bien, renvoie un message pour que nous soyons sûr que tout va bien.")
                            if self.game_master:
                                messagebox.showwarning("Sans nouvelles d'un joueur",
                                                       f"{player.name} {player.lastname} n'a plus envoyé de messages depuis {self.config['min_before_inactiv_warn'] * player.warnings} minutes. Un message d'avertissement lui a été envoyé. Une procédure d'urgence aura lieu automatiquement si on n'a pas de nouvelles dans {self.config['max_warns'] - player.warnings * self.config['min_before_inactiv_warn']} minutes")
                        player.warnings += 1
                        player.last_warning = int(datetime.datetime.now().timestamp())
                if self.receive:
                    Timer(5, recieve).start()

        Timer(2, recieve).start()


if __name__ == '__main__':
    SMSGame(True)
