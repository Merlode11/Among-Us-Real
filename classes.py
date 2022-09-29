import json
import time
from tkinter import messagebox
from smsManager import send_sms, get_new_messages
from commands import commands
import random


class Player:
    def __init__(self, name: str, lastname: str, phone: str):
        self.name: str = name
        self.lastname: str = lastname
        self.phone: str = phone
        self.tasks: list = []
        self.role: str = ""
        self.dead: bool = False
        self.asks: int = 0
        self.last_message: int = 0
        self.warnings: int = 0

    def __repr__(self):
        return f"Player({self.name}, {self.lastname}, {self.phone})"

    def get_str(self, game):
        if game.game_master:
            if self.dead:
                return f"☠ {self.name} {self.lastname} ({game.config['names'][self.role]}): {self.phone}"
            return f"{self.name} {self.lastname} ({game.config['names'][self.role]}): {self.phone}"
        else:
            if self.dead and not game.config["show_dead_roles"]:
                return f"☠️ {self.name} {self.lastname}: {self.phone}"
            elif self.dead:
                return f"☠️ {self.name} {self.lastname} ({game.config['names'][self.role]}): {self.phone}"
        return f"{self.name} {self.lastname}: {self.phone}"

    def finished_all_tasks(self):
        finished = 0
        for task in self.tasks:
            if task.done:
                finished += 1
        return finished == len(self.tasks)


class Task:
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


class Game:
    def __init__(self):
        with open("players.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            self.players = [Player(player["name"], player["lastname"], player["phone"]) for player in data if
                            player.get("play")]

        with open("config.json", "r", encoding='utf-8') as f:
            self.config = json.load(f)

        self.tasks: list = []
        with open(r"/taskList/" + self.config["task_list"] + ".json", "r", encoding='utf-8') as f:
            data = json.load(f)
            self.tasks = [Task(task["name"], task["description"], task["type"], task["location"], task.get("other")) for
                          task in data]

        self.given_tasks: int = 0

        self.crewmates: list = []
        self.impostors: list = []
        self.dead_players: list = []
        self.done_tasks: list = []
        self.receive: bool = True
        self.send_messages: list = []
        self.meeting: int = None

        self.game_master: bool = self.config["game_master"]
        self.pause: bool = False

    def define_roles(self):
        random.shuffle(self.players)
        for i in range(self.config["impostors"]):
            self.impostors.append(self.players[i])
            self.players[i].role = "impostor"
        self.crewmates = self.players[self.config["impostors"]:]

        for player in self.crewmates:
            player.role = "crewmate"
        for player in self.impostors:
            player.role = "impostor"

        for i in range(self.config["ingenors"]):
            self.crewmates[i].role = "ingenior"
        for i in range(self.config["scientists"]):
            self.crewmates[i + self.config["ingenors"]].role = "scientist"

        self.players = sorted(self.players, key=lambda joueur: joueur.name)

    def define_tasks(self):
        for player in self.players:
            random.shuffle(self.tasks)
            for i in range(self.config["tasks"]):
                player.tasks.append(Task(self.tasks[i].name, self.tasks[i].description, self.tasks[i].classe,
                                         self.tasks[i].location, self.tasks[i].other))
                self.tasks[i].nb_given += 1
                if self.tasks[i].nb_given >= self.config["max_task_given"]:
                    del self.tasks[i]
            if player.role != "impostor":
                self.given_tasks += self.config["tasks"]
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
            message += "Pour voir toutes les commandes, vous pouvez taper \"help\"\n"
            message += "Nous vous souhaitons une bonne partie !"

            self.send_messages.append(message)
            # send_sms(player.phone, message)

    def send_message_to_all(self, message: str):
        for player in self.players:
            self.send_messages.append(message)
            send_sms(player.phone, message)

        messagebox.showinfo("Succès", "Le message a été envoyé à tout le monde !")

    def check_command(self, player, message):
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
        from threading import Timer

        def test():
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
                if player.last_message + self.config["min_before_inactiv_warn"] * 60 < time.now():
                    if player.warnings >= self.config["max_warns"]:
                        self.send_message_to_all(
                            f"{player.name} {player.lastname} n'a pas donné de ses nouvelles depuis {self.config['min_before_inactiv_warn'] * player.warnings} minutes. Le jeu est donc en pause le temps qu'on retrouve le joueur")
                        self.pause = True
                        messagebox.showerror("Un joueur ne répond pas",
                                             f"{player.name} {player.lastname} n'a pas donné de ses nouvelles depuis {self.config['min_before_inactiv_warn'] * player.warnings} minutes. Le jeu est donc en pause le temps qu'on retrouve le joueur. Un message a été envoyé à tout le monde.")

                    else:
                        send_sms(player.phone,
                                 f"Il y a un problème ? Nous n'avons pas reçu de message depuis {self.config['min_before_inactiv_warn'] * player.warnings} minutes. Si tout va bien, renvoie un message pour que nous soyons sûr que tout va bien.")
                        messagebox.showwarning("Sans nouvelles d'un joueur",
                                               f"{player.name} {player.lastname} n'a plus envoyé de messages depuis {self.config['min_before_inactiv_warn'] * player.warnings} minutes. Un message d'avertissement lui a été envoyé. Une procédure d'urgence aura lieu automatiquement si on n'a pas de nouvelles dans {self.config['max_warns'] - player.warnings * self.config['min_before_inactiv_warn']} minutes")
                    player.warnings += 1
            if self.receive:
                Timer(2, test).start()

        test()
