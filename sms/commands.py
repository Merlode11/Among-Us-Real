from tkinter import messagebox
from airmore_manager import send_sms
import re  # Importation du module pour faire des tests d'expressions régulières


class Command:
    """
    Initialisation de la classe commande
    """

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

    def run(self, player, message: str, game) -> bool:
        """
        Exécute la commande avec une vérification du rôle et de la partie
        :param player: Le joueur qui a effecuté la commande
        :param message: str: Le string envoyé par le message
        :param game: La partie
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
        elif game.meeting and self.name not in ["help", "sos"]:
            send_sms(player.phone, "Une réunion est en cours. Vous ne pouvez pas faire de commandes")
            return True
        else:
            self.execute(player, message, game)
            return True

    def execute(self, player, message: str, game):
        """
        Exécute la commande
        :param player: Le joueur qui a effecuté la commande
        :param message: str: Le string envoyé par le message
        :param game: La partie
        """
        pass


commands: list = []


class TaskCommand(Command):
    """
    Affiche plus d'informations sur une tâche demandée
    """

    def __init__(self):
        super().__init__("task", "Permet de voir la description d'une tâche",
                         ["tâche", "détail", "detail", "task", "tache"],
                         "task NOMBRE", "task 1")

    def execute(self, player, message: str, game) -> None:
        """
        Commande permettant d'avoir plus d'informations sur la tâche à effectuer
        :param player: Le joueur qui a exécuté la commande
        :param message: str: Le message envoyé par le joueur
        :param game: La partie
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
    """
    Affiche les informations sur les tâches restantes
    """

    def __init__(self):
        super().__init__("info", "Permet de voir les tâches restantes", ["restant", "last", "reste"], "info", "info")

    def execute(self, player, message: str, game) -> None:
        """
        Commande permettant d'avoir plus d'informations sur la tâche à effectuer
        :param player: Le joueur qui a exécuté la commande
        :param message: str: Le message envoyé par le joueur
        :param game: La partie
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

        string += f"Il reste {len(game.done_tasks)}/{game.given_tasks} tâche pour les {game.config['names']['crewmate']}."

        string += f"\nVotre identifiant est {player.id}."
        send_sms(player.phone, string)


commands.append(InfoCommand())


class DeadsCommand(Command):
    """
    Affiche pour chaque joueur si jamais il est en vie ou non
    """

    def __init__(self):
        super().__init__("deads", "Voir les états de chaque joueur", ["view", "states", "états", "morts"], "deads",
                         "deads",
                         "scientist")

    def execute(self, player, message: str, game) -> None:
        """
        Commande qui renvoie l'état des personnes pour le rôle "Scientifique"
        :param player: Le joueur qui a exécuté la commande
        :param message: str: Le message envoyé par le joueur
        :param game: La partie
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
    """
    Acte comme le signalement d'un cadavre par la personne
    """

    def __init__(self):
        super().__init__("mort", "Annonce à l'organisateur la découverte d'un corps", ["death", "cadavre", "corps"],
                         "mort PERSONNE", "mort 1")

    def execute(self, player, message: str, game) -> None:
        """
        Commande pour signaler une personne morte
        :param player: Le joueur qui a exécuté la commande
        :param message: str: Le message envoyé par le joueur
        :param game: La partie
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
                dead_id = int(dead_str[0]) - 1
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
    """
    Valide une tâche comme effectuée
    """

    def __init__(self):
        super().__init__("done", "Valide une tâche comme faite", ["fait", "réalisé"], "done NOMBRE", "done 1")

    def execute(self, player, message: str, game) -> None:
        """
        Commande pour déclarer qu'une tâche a été effectuée
        :param player: Le joueur qui a exécuté la commande
        :param message: str: Le message envoyé par le joueur
        :param game: La partie
        """
        try:
            task_number = int(message.split(" ")[1])
            task = player.tasks[task_number - 1]
            if task.done:
                send_sms(player.phone, "Vous avez déjà déclaré avoir fait la tâche " + str(task_number))
            elif "valid" in task.type:
                send_sms(player.phone, "Vous ne pouvez pas déclarer avoir fait la tâche " + str(task_number) + " par une commande")
            elif task.type == "activate_basic" and not task.active:
                send_sms(player.phone, "Vous ne pouvez pas déclarer avoir fait la tâche " + str(task_number) + " car elle n'est pas encore active")
            else:
                game.done_task(player, task)
                game.send_info(player, f"Votre tâche {task.name} a été confirmée comme faite !")
        except (Exception,):
            send_sms(player.phone, "Veuillez entrer un numéro de tâche valide !")


commands.append(DoneCommand())


class HelpCommand(Command):
    """
    Affiche la page d'aide pour toutes les commandes ou pour une commande spécifique
    """

    def __init__(self):
        super().__init__("help", "Obtenir toutes les commandes et de l'aide pour chacune",
                         ["aide", "commandes", "commande", "commands", "command"], "help (COMMANDE)", "help help")

    def execute(self, player, message: str, game) -> None:
        """
        Commande qui renvoie toutes les commandes disponibles
        :param player: Le joueur qui a exécuté la commande
        :param message: str: Le message envoyé par le joueur
        :param game: La partie
        """
        if len(message.split(" ")) == 1:
            string = "Voici toutes les commandes disponibles:\n"
            for command in commands:
                string += command.usage + ": " + command.description + "\n"
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


class SOSCommand(Command):
    """
    Permet aux joueurs de demander de l'aide aux autres joueurs en cas de problèmes urgent
    """

    def __init__(self):
        super().__init__(
            "sos",
            "Commande d'URGENCE pour signaler que vous avez un problème",
            ["urgence", "problème", "prob", "problem"],
            "sos (LOCALISATION - MESSAGE)",
            "sos maison problème de jambe")

    def execute(self, player, message: str, game) -> None:
        """
        Commande qui demande de l'aide aux autres joueurs
        :param player: Le joueur qui a exécuté la commande
        :param message: str: Le message envoyé par le joueur
        :param game: La partie
        """
        game.send_message_to_all(
            f"{player.name} {player.lastname} a besoin d'aide en URGENCE ! Son message:\n{' '.join(message.split(' ')[1:])}")
        game.pause = True
        code = game.set_pause_game()
        send_sms(player.phone,
                 f"Votre demande d'aide a bien été transmise aux autres joueurs. Le code pour rétablir la partie normalement est '{code}'")
        if game.game_master:
            messagebox.showerror(f"{player.name} {player.lastname} a besoin d'aide",
                                 f"{player.name} {player.lastname} a demandé de l'aide en URGENCE avec la commande SOS. Son message:\n{' '.join(message.split(' ')[1:])}\n\nUn message a été envoyé à tous les joueurs pour aller l'aider et la partie a été mise en pause")


class KillCommand(Command):
    """
    Permet aux imposteurs de tuer une personne
    """

    def __init__(self):
        super().__init__(
            "kill",
            "Tuer une personne, si elle est à côté de vous",
            ["tuer", "murder", "stab"],
            "kill PERSONNE",
            "kill Merlode",
            "impostor"
        )

    def execute(self, player, message: str, game):
        """
        Tuer une personne 
        """
        player_id = re.match(r"\d{3}", message.split(" ")[1])
        print(player_id[0])
        to_kill_player = None
        for joueur in game.players:
            if joueur.id == player_id[0]:
                to_kill_player = joueur
        if to_kill_player:
            if to_kill_player.id == player.id:
                send_sms(player.phone, "Vous ne pouvez pas vous tuer vous-même")
                return
            else:
                game.kill_player(to_kill_player)
                send_sms(player.phone, f"Le joueur {to_kill_player.name} {to_kill_player.lastname} a bien été tué de votre part !")
        else:
            send_sms(player.phone,
                     "Ce joueur n'a pas été trouvé ?! Merci de vérifier que la personne a bien donné son matricule.")


commands.append(KillCommand())


class VoteCommand(Command):
    def __init__(self):
        super(VoteCommand, self).__init__(
            "vote",
            "Voter pour une personne durant les phases de meeting",
            ["voter", "voté", "votée", "votés"],
            "vote PERSONNE",
            "vote 1"
        )

    def execute(self, player, message: str, game):
        """
        Voter pour une personne
        """
        if game.meeting != "vote":
            send_sms(player.phone, "Il n'y a pas de période de vote en cours !")
            return
        else:
            if player.id in game.meeting_votes.keys():
                send_sms(player.phone, "Vous avez déjà voté !")
                return
            else:
                if message.split(" ")[1] == "0" or message.split(" ")[1] == "skip" or message.split(" ")[1] == "passer":
                    game.meeting_votes[player.id] = "0"
                    send_sms(player.phone, "Vous avez voté pour passer !")
                voted_player: list = parse_player(message, game)
                if len(voted_player) > 1:
                    players_str = ""
                    for i, player in enumerate(voted_player):
                        players_str += f"{i + 1} - {player.name} {player.lastname}\n"
                    send_sms(player.phone, f"Plusieurs joueurs ont été trouvés:\n{players_str}Veuillez réessayer en précisant le numéro du joueur:\nvote NUMERO")
                    return
                elif voted_player is None or len(voted_player) == 0:
                    send_sms(player.phone, "Aucun joueur n'a été trouvé avec ce nom !")
                    return
                else:
                    voted_player = voted_player[0]
                    game.meeting_votes[player.id] = voted_player.id
                    send_sms(player.phone, f"Vous avez voté pour {voted_player.name} {voted_player.lastname} !")
                    game.timer.show_players()
                    return


commands.append(VoteCommand())


def parse_player(message: str, game) -> list:
    """
    Trouve un joueur donné un argument dans une commande
    :param message: str: Le message envoyé par le joueur
    :param game: La partie
    :return SMSPlayer or None or str: Le joueur si trouvé
    """
    try:
        player_id = int(message.split(" ")[1])
        player = game.players[player_id - 1]
        return [player]
    except (Exception,):
        player_name = message.split(" ")[1].lower()
        found_players = []
        for i in range(game.players):
            player = game.players[i]
            if player.name.lower() == player_name or player.lastname.lower() == player_name:
                player_with_id = (i + 1, player)
                found_players.append(player_with_id)

        return found_players