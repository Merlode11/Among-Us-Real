import json
import datetime
from tkinter import messagebox
from smsManager import send_sms, get_new_messages
from commands import commands
import random
from tkinter import *
from utils import clear_frame, VerticalScrolledFrame, show_timer


class Game:
    def __init__(self):
        self.players: list = []
        self.import_players()

        with open("config.json", "r", encoding='utf-8') as f:
            self.config = json.load(f)

        self.tasks: list = []
        with open(r"./taskList/" + self.config["task_list"] + ".json", "r", encoding='utf-8') as f:
            data = json.load(f)
            self.tasks = [
                BasicTask(task["name"], task["description"], task["type"], task["location"], task.get("other")) for
                task in data]

        self.given_tasks: int = 0

        self.crewmates: list = []
        self.impostors: list = []
        self.dead_players: list = []
        self.done_tasks: list = []
        self.receive: bool = True
        self.send_messages: list = []
        self.meeting: bool = False

        self.game_master: bool = self.config["game_master"]
        self.pause: bool = False
        self.unpause_code: str = ""

    def define_roles(self) -> None:
        """
        Défini les rôles de chacun des participants
        """
        random.shuffle(self.players)
        for i in range(self.config["impostors"]):
            self.impostors.append(self.players[i])
            self.players[i].role = "impostor"
        self.crewmates = self.players[self.config["impostors"]:]

        for player in self.crewmates:
            player.role = "crewmate"
        for player in self.impostors:
            player.role = "impostor"

        for i in range(self.config["ingeniors"]):
            self.crewmates[i].role = "ingenior"
        for i in range(self.config["scientists"]):
            self.crewmates[i + self.config["ingeniors"]].role = "scientist"

        self.players = sorted(self.players, key=lambda joueur: joueur.name)

    def define_tasks(self) -> None:
        """
        Défini les tâches du joueur pour chaque participant
        """
        for player in self.players:
            random.shuffle(self.tasks)
            for i in range(self.config["tasks"]):
                player.tasks.append(BasicTask(self.tasks[i].name, self.tasks[i].description, self.tasks[i].classe,
                                              self.tasks[i].location, self.tasks[i].other))
                self.tasks[i].nb_given += 1
                if self.tasks[i].nb_given >= self.config["max_task_given"]:
                    del self.tasks[i]
            if player.role != "impostor":
                self.given_tasks += self.config["tasks"]
            self.send_role(player)

    def send_role(self, player):
        pass

    def set_pause_game(self):
        """
        Définir le code d'arrêt de la partie
        """
        code_int = random.randint(0, 1000)
        code_str = f"{code_int}"
        self.unpause_code = code_str
        return code_str

    def start_meeting(self):
        window = Tk()
        window.title("Réunion")
        window.geometry("500x500")
        window.resizable(False, False)
        window.state("zoomed")
        window.iconbitmap("assets/img/amongus.ico")
        window.config(background="#2F3136")

        Label(window, text="Réunion", font=("Arial", 30), bg="#2F3136", fg="white").pack()
        Label(window, text="Veuillez choisir un joueur à éliminer", font=("Arial", 20), bg="#2F3136", fg="white").pack()
        Label(window, text="ou appuyer sur le bouton pour passer", font=("Arial", 20), bg="#2F3136", fg="white").pack()
        Label(window, text="à la prochaine étape", font=("Arial", 20), bg="#2F3136", fg="white").pack()

        players_here_frame = VerticalScrolledFrame(window, bg="#2F3136")
        here_users = []

        def show_players():
            clear_frame(players_here_frame)
            print(self.players)
            for player in self.players:
                print(player.name, ":", player.password)
                if player in here_users:
                    color = "green"
                else:
                    color = "red"
                if player.dead:
                    Label(players_here_frame, text=player.get_str(self), font=("Arial", 20, "italic"), bg="#2F3136", fg=color).pack()
                else:
                    Label(players_here_frame, text=player.get_str(self), font=("Arial", 20), bg="#2F3136", fg=color).pack()

        def present(password: str):
            for player in self.players:
                if player.password == password:
                    if player in here_users:
                        messagebox.showerror("Erreur", "Vous êtes déjà présent")
                    else:
                        here_users.append(player)
                    show_players()
                    present_entry.delete(0, END)

                    if len(here_users) == len(self.players):
                        window.destroy()
                        show_timer(self.config.get("discussion_time", 0), "Discussion")
                        vote_string = "C'est le moment de voter ! Votez pour le joueur à éliminer:"
                        vote_string += "\n0 - Passer à la prochaine étape (skip)"
                        for i in range(len(self.players)):
                            player = self.players[i]
                            if not player.dead:
                                vote_string += f"\n{i + 1} - {player.name}"
                        vote_string += f"\n\nVotez avec la commande 'vote NUMERO'"
                        self.send_info(vote_string)
                        show_timer(self.config.get("vote_time", 0), "Vote")
                    return
            else:
                messagebox.showerror("Erreur", "Mot de passe incorrect")

        Label(window, text="", bg="#2F3136").pack()
        present_label = Label(window, text="Indiquer que vous êtes présent :", font=("Arial", 20), bg="#2F3136", fg="white")
        present_entry = Entry(window, font=("Arial", 20), bg="#4f5259", fg="white")
        present_button = Button(window, text="Valider", font=("Arial", 20), bg="#2F3136", fg="white", command=lambda: present(present_entry.get()))
        present_label.pack()
        present_entry.pack()
        present_button.pack()

        present_entry.bind("<Return>", lambda event: present(present_entry.get()))

        show_players()

        Label(window, text="", bg="#2F3136").pack()

        players_here_frame.pack()

        window.mainloop()

    def import_players(self):
        used_passwords: list = []
        used_id: list = []
        with open("players.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            self.players = [SMSPlayer(player["name"], player["lastname"], player["phone"], used_passwords, used_id)
                            for player in data if player.get("play", True)]
        for player in self.players:
            player_id = random.randint(0, 999)
            while player_id in used_id:
                player_id = random.randint(0, 999)
            used_id.append(player_id)
            player.id = f"{player_id:03}"

    def send_info(self, message: str):
        print("Envoie de l'information")
        for player in self.players:
            print(player.name, ":", message)


class SMSGame(Game):
    def import_players(self):
        used_passwords: list = []
        used_id: list = []
        with open("players.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            self.players = [SMSPlayer(player["name"], player["lastname"], player["phone"], used_passwords, used_id)
                            for player in data if player.get("play", True)]
        for player in self.players:
            player_id = random.randint(0, 999)
            while player_id in used_id:
                player_id = random.randint(0, 999)
            used_id.append(player_id)
            player.id = f"{player_id:03}"

    def send_role(self, player) -> None:
        """
        Envoie un sms au joueur indiquant son role et ses tâches
        :param player: SMSPlayer: Le joueur avec son numéro de téléphone
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
        send_sms(player.phone, message)

    def send_message_to_all(self, message: str) -> None:
        """
        Envoie un message à tous les joueurs
        :param message: str: Le message à envoyer
        """
        for player in self.players:
            self.send_messages.append(message)
            send_sms(player.phone, message)

        if self.game_master:
            messagebox.showinfo("Succès", "Le message a été envoyé à tout le monde !")

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
            if task.get("other") and task["other"].get("keywords"):
                for word in task["other"]["keywords"]:
                    if word in message:
                        task.done = True
                        self.done_tasks.append(task)
                        send_sms(player.phone, f"Votre tâche {task.name} a été confirmée comme faite !")
                        messagebox.showinfo("Succès",
                                            f"{player.name} {player.lastname} a confirmé avoir réalisé la tâche {task.name} ! Son message est :\n {message}")
                        return True
        return False

    def start_recieve_sms(self):
        """
        Active la vérification périodique de la réception de SMS
        """
        from threading import Timer

        def recieve():
            new = get_new_messages(self)
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
                if player.last_message + self.config["min_before_inactiv_warn"] * 60 < datetime.date.today():
                    if player.warnings >= self.config["max_warns"]:
                        self.send_message_to_all(
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
                if self.receive:
                    Timer(2, recieve).start()
            recieve()


class WebGame(Game):
    def __init__(self, ip: str, port: int):
        super().__init__()
        self.ip = ip
        self.port = port
        self.server = None
        self.receive = False


class Player:
    def __init__(self, used_passwords: list):
        self.tasks: list = []
        self.role: str = ""
        self.dead: bool = False
        self.asks: int = 0
        self.last_message: int = 0
        self.warnings: int = 0
        self.id: str = "0"

        self.password: str = "".join([str(random.randint(0, 9)) for _ in range(8)])
        while self.password in used_passwords:
            self.password = "".join([str(random.randint(0, 9)) for _ in range(8)])
        used_passwords.append(self.password)

    def __repr__(self) -> str:
        """
        Affiche la classe Player telle qu'elle doit être déclarée pour ce joueur
        :return: str: Le string de l'affichage
        """
        return f"Player()"

    def get_str(self, game: Game):
        pass

    def finished_all_tasks(self) -> bool:
        """
        Renvoie si le joueur a fini toutes ses tâches
        :return: bool: True s'il a fini toutes ses tâches, False sinon
        """
        finished = 0
        for task in self.tasks:
            if task.done:
                finished += 1
        return finished == len(self.tasks)


class SMSPlayer(Player):
    def __init__(self, name: str, lastname: str, phone: str, used_passwords: list, used_ids: list):
        super().__init__(used_passwords)
        self.name: str = name
        self.lastname: str = lastname
        self.phone: str = phone

    def get_str(self, game: SMSGame) -> str:
        if game.game_master:
            if self.dead:
                return f"☠ {self.name} {self.lastname} ({game.config['names'][self.role]}): {self.phone}"
            return f"{self.name} {self.lastname} ({game.config['names'][self.role]}): {self.phone}"
        else:
            if self.dead and not game.config["show_dead_roles"]:
                return f"☠ {self.name} {self.lastname}: {self.phone}"
            elif self.dead:
                return f"☠ {self.name} {self.lastname} ({game.config['names'][self.role]}): {self.phone}"
        return f"{self.name} {self.lastname}: {self.phone}"


class WebPlayer(Player):
    def __init__(self, ip: str, nickname: str, color: str, used_passwords: list):
        super().__init__(used_passwords)
        self.ip: str = ip
        self.nickname: str = nickname
        self.color: str = color
        self.id: str = color

    def get_str(self, game: WebGame) -> str:
        if game.game_master:
            if self.dead:
                return f"☠ {self.nickname} ({self.ip}), {game.config['names'][self.role]}"
            return f"{self.nickname} ({self.ip}), {game.config['names'][self.role]}"
        else:
            if self.dead and not game.config["show_dead_roles"]:
                return f"☠ {self.nickname} ({self.ip})"
            elif self.dead:
                return f"☠ {self.nickname} ({self.ip}), {game.config['names'][self.role]}"
        return f"{self.nickname} ({self.ip})"


class BasicTask:
    type: str = "basic"

    def __init__(self, name: str, description: str, classe: str, location: str, other: dict = None):
        self.name: str = name
        self.description: str = description
        self.classe: str = classe
        self.location: str = location
        self.done: bool = False
        self.other: dict = other
        self.nb_given: int = 0
        self.success: int = 0

        if self.other and self.other.get("questions"):
            random.shuffle(self.other["questions"])
            questions = []
            for i in range(3):
                questions.append(self.other["questions"][i])
            self.other["questions"] = questions

    def __repr__(self):
        return f"{self.name} ({self.classe}): {self.description} | {self.location}"

    def __str__(self):
        return f"{self.name} ({self.classe})"


class ValidateBasicTask(BasicTask):
    type: str = "validate_basic"

    def __init__(self, name: str, description: str, classe: str, location: str, valid_keywords: list):
        super().__init__(name, description, classe, location, {})
        self.keywords: list = valid_keywords

    def __repr__(self):
        return f"ValidateBasicTask({self.name}, {self.description}, {self.classe}, {self.location}, {self.other})"

    def __str__(self):
        return f"Valide la tâche {self.name} ({self.classe})"


class ActivateBasicTask(BasicTask):
    type: str = "activate_basic"

    def __init__(self, name: str, description: str, classe: str, location: str, activ_keywords: list, message: str):
        super().__init__(name, description, classe, location, {})
        self.activ_keywords: list = activ_keywords
        self.message: str = message

    def __repr__(self):
        return f"ActivateBasicTask({self.name}, {self.description}, {self.classe}, {self.location}, {self.other})"

    def __str__(self):
        return f"Active la tâche {self.name} ({self.classe})"


class ActivValidTask(ValidateBasicTask):
    type: str = "activ_valid"

    def __init__(self, name: str, description: str, classe: str, location: str, valid_keywords: list,
                 activ_keywords: list, message: str):
        super().__init__(name, description, classe, location, valid_keywords)
        self.activ_keywords: list = activ_keywords
        self.message: str = message

    def __repr__(self):
        return f"ActivValidTask({self.name}, {self.description}, {self.classe}, {self.location}, {self.other})"

    def __str__(self):
        return f"Active et valide la tâche {self.name} ({self.classe})"

class CustomValidateTask(BasicTask):
    type: str = "custom_validate"

    def __init__(self, name: str, description: str, classe: str, location: str, valid_keywords: list, message: str):
        super().__init__(name, description, classe, location, {})
        self.keywords: list = valid_keywords
        self.message: str = message

    def __repr__(self):
        return f"CustomValidateTask({self.name}, {self.description}, {self.classe}, {self.location}, {self.other})"

    def __str__(self):
        return f"Valide la tâche {self.name} ({self.classe})"


if __name__ == "__main__":
    game = Game()
    game.start_meeting()
