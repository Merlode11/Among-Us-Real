from tkinter import messagebox, ttk
from smsManager import send_sms
from collections.abc import Callable
from classes import SMSGame, SMSPlayer


class Command:
    def __init__(self,
                 name: str,
                 description: str,
                 aliases: list,
                 usage: str,
                 exemple: str,
                 permission: str = None):
        self.name: str = name
        self.description: str = description
        self.aliases: list = aliases
        self.usage: str = usage
        self.exemple: str = exemple
        self.permission: str = permission

    def get_help(self, config: dict = None) -> str:
        """
        Affiche la page d'aide pour la commande
        :param config: dict: la configuration du jeu
        :return: str: Le string avec l'aide de la commande
        """
        string: str = "Voici la page d'aide pour la commande " + self.name + ":"
        string += "\n" + self.description
        string += "\nAlias :" + ", ".join(self.aliases)
        if self.permission:
            string += "\nUtilisable par :"
            if config is not None and config.get("names") and config["names"].get(self.permission.lower()):
                string += config["names"][self.permission.lower()]
            else:
                string += self.permission
        string += "\nUtilisation:" + self.usage + " (" + self.exemple + ")"
        return string

    def run(self, player: SMSPlayer, message: str, game: SMSGame) -> bool:
        """
        Exécute la commande avec une vérification du rôle et de la partie
        :param player: SMSPlayer: Le joueur qui a effecuté la commande
        :param message: str: Le string envoyé par le message
        :param game: SMSGame: La partie
        :return: bool: Renvoie la bonne utilisation de la commande
        """
        # Check permission
        if self.permission and player.role != self.permission:
            perm: str = self.permission
            if game.config.get("names") and game.config["names"].get(self.permission.lower()):
                perm = game.config["names"][self.permission.lower()]

            send_sms(player.phone, "Vous ne pouvez pas utiliser cette commande car vous n'êtes pas" + perm + " !")
            return True
        elif game.pause and self.name not in ["help", "sos"]:
            send_sms(player.phone, "La partie est actuellement en pause. Vous ne pouvez pas faire de commandes")
            return True
        else:
            self.execute(player, message, game)
            return True

    def execute(self, player: SMSPlayer, message: str, game: SMSGame):
        """
        Exécute la commande
        :param player: SMSPlayer: Le joueur qui a effecuté la commande
        :param message: str: Le string envoyé par le message
        :param game: SMSGame: La partie
        """
        pass


commands: list = []


class TaskCommand(Command):
    def __init__(self):
        super().__init__("task", "Permet de voir la description d'une tâche",
                         ["tâche", "détail", "detail", "task", "tache"],
                         "task NOMBRE", "task 1")

    def execute(self, player: SMSPlayer, message: str, game: SMSGame) -> None:
        """
        Commande permettant d'avoir plus d'informations sur la tâche à effectuer
        :param player: SMSPlayer: Le joueur qui a exécuté la commande
        :param message: str: Le message envoyé par le joueur
        :param game: SMSGame: La partie
        """
        try:
            task_number = int(message.split(" ")[1])
            task = player.tasks[task_number - 1]
            string = f"{task.name} ({task.classe})\n"
            string += f"Lieu: {task.location}\n"
            string += f"Description: {task.description}\n"
            send_sms(player.phone, string)
        except (Exception,):
            send_sms(player.phone, "Veuillez entrer un numéro de tâche valide !")


commands.append(TaskCommand())


class InfoCommand(Command):
    def __init__(self):
        super().__init__("info", "Permet de voir les tâches restantes", ["restant", "last", "reste"], "info", "info")

    def execute(self, player: SMSPlayer, message: str, game: SMSGame) -> None:
        """
        Commande permettant d'avoir plus d'informations sur la tâche à effectuer
        :param player: SMSPlayer: Le joueur qui a exécuté la commande
        :param message: str: Le message envoyé par le joueur
        :param game: SMSGame: La partie
        """
        remining = 0
        done = 0
        string = ""
        for i in range(len(player.tasks)):
            task = player.tasks[i]
            if task.done:
                done += 1
            else:
                remining += 1
                string += f"{i + 1}: {task.name} ({task.classe})\n"
        string = f"Il vous reste {remining} tâches à accomplir.\n" + string
        if done == len(player.tasks):
            string += "Vous avez accompli toutes vos tâches !\n"

        string += f"Il reste {len(player.done_tasks)}/{player.given_tasks} tâche pour les " + game.config["names"][
            "crewmate"] + "."
        send_sms(player.phone, string)


commands.append(InfoCommand())


class DeadsCommand(Command):
    def __init__(self):
        super().__init__("deads", "Voir les états de chaque joueur", ["view", "states", "états", "morts"], "deads",
                         "deads",
                         "scientist")

    def execute(self, player: SMSPlayer, message: str, game: SMSGame) -> None:
        """
        Commande qui renvoie l'état des personnes pour le rôle "Scientifique"
        :param player: SMSPlayer: Le joueur qui a exécuté la commande
        :param message: str: Le message envoyé par le joueur
        :param game: SMSGame: La partie
        """
        if player.asks >= game.config["max_dead_check"]:
            send_sms(player.phone, "Vous avez utilisé toutes vos demandes !")
        else:
            states = "Voici les états de chaque joueur:\n"
            for joueur in game.players:
                if joueur.dead:
                    states += "- " + joueur.name + " " + joueur.lastname + " (mort)\n"
                else:
                    states += "- " + joueur.name + " " + joueur.lastname + " (vivant)\n"
            player.asks += 1
            states += "\n Il vous reste " + str(game.config["max_dead_check"] - player.asks) + "/" + str(
                game.config["max_dead_check"]) + " demandes."
            send_sms(player.phone, states)


commands.append(DeadsCommand())


class MortCommand(Command):
    def __init__(self):
        super().__init__("mort", "Annonce à l'organisateur la découverte d'un corps", ["death", "cadavre", "corps"],
                         "mort PERSONNE", "mort 1")

    def execute(self, player: SMSPlayer, message: str, game: SMSGame) -> None:
        """
        Commande pour signaler une personne morte
        :param player: SMSPlayer: Le joueur qui a exécuté la commande
        :param message: str: Le message envoyé par le joueur
        :param game: SMSGame: La partie
        """
        if game.game_master:
            response = messagebox.askokcancel("Mort détecté",
                                              f"{player.name} {player.lastname} découvert un corps ! Son message est :\n {message}")
            if response == "ok":
                game.send_message_to_all(
                    "Un cadavre a été signalé.\nMerci de vous rendre immédiatement au point de rendez vous !")
            elif response == "cancel":
                send_sms(player.phone, "Votre demande a été refusée par l'organisateur.ice")
        else:
            dead_str = message.split(" ")[1:]
            try:
                dead_id = dead_str[0] - 1
                dead = game.players[dead_id]
                if not dead.dead:
                    send_sms(player.phone, "Ce joueur ne peux pas être déclaré comme cadavre car il n'est pas mort")
                    return
                else:
                    send_sms(player.phone, "Ce joueur ne peux pas être déclaré comme cadavre car il n'est pas mort")
            except (Exception,):
                send_sms(player.phone, "Veuillez entrer un joueur valide !")


commands.append(MortCommand())


class DoneCommand(Command):
    def __init__(self):
        super().__init__("done", "Valide une tâche comme faite", ["fait", "réalisé"], "done NOMBRE", "done 1")

    def execute(self, player: SMSPlayer, message: str, game: SMSGame) -> None:
        """
        Commande pour déclarer qu'une tâche a été effectuée
        :param player: SMSPlayer: Le joueur qui a exécuté la commande
        :param message: str: Le message envoyé par le joueur
        :param game: SMSGame: La partie
        """
        try:
            task_number = int(message.split(" ")[1])
            task = player.tasks[task_number - 1]
            if task.done:
                send_sms(player.phone, "Vous avez déjà déclaré avoir fait la tâche " + str(task_number))
            else:
                task.done = True
                game.done_tasks.append(task)
                send_sms(player.phone, f"Votre tâche {task.name} a été confirmée comme faite !")
                if game.game_master:
                    messagebox.showinfo("Succès",
                                        f"{player.name} {player.lastname} a confirmé avoir réalisé la tâche {task.name} ! Son message est :\n {message}")
        except (Exception,):
            send_sms(player.phone, "Veuillez entrer un numéro de tâche valide !")


commands.append(DoneCommand())


class HelpCommand(Command):
    def __init__(self):
        super().__init__("help", "Obtenir toutes les commandes et de l'aide pour chacune",
                         ["aide", "commandes", "commande", "commands", "command"], "help (COMMANDE)", "help help")

    def execute(self, player: SMSPlayer, message: str, game: SMSGame) -> None:
        """
        Commande qui renvoie toutes les commandes disponibles
        :param player: SMSPlayer: Le joueur qui a exécuté la commande
        :param message: str: Le message envoyé par le joueur
        :param game: SMSGame: La partie
        """
        if len(message.split(" ")) == 1:
            string = "Voici toutes les commandes disponibles:\n"
            for command in commands:
                string += command.exemple + ": " + command.description
            send_sms(player.phone, string)
        else:
            command_str = message.split(" ")[1]
            command = None
            for cmd in commands:
                if command_str in ([cmd.name] + cmd.aliases):
                    command = cmd
                    break
            string = command.get_help(game.config)
            send_sms(player.phone, string)


commands.append(HelpCommand())
