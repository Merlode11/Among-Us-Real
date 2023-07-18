import time
from tkinter import messagebox
import re  # Importation du module pour faire des tests d'expressions régulières
from whatsapp.whatsapp_manager import sendMessage

kills_cooldown = {}


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
        string += "\nAlias: " + ", ".join(self.aliases)
        if self.permission:
            string += "\nUtilisable par: "
            if config is not None and config.get("names") and config["names"].get(self.permission.lower()):
                string += config["names"][self.permission.lower()]
            else:
                string += self.permission
        string += "\nUtilisation: " + self.usage + " (exemple: " + self.exemple + ")"
        return string

    def run(self, player, content: str, message, game) -> bool:
        """
        Exécute la commande avec une vérification du rôle et de la partie
        :param player: Le joueur qui a effecuté la commande
        :param content: str: Le string envoyé par le message
        :param message: dict: Le message envoyé
        :param game: La partie
        :return: bool: Renvoie la bonne utilisation de la commande
        """
        is_necessary = self.name in ["help", "sos"]
        # Check permission
        if self.permission and player.role != self.permission:
            perm: str = self.permission
            if game.config.get("names") and game.config["names"].get(self.permission.lower()):
                perm = game.config["names"][self.permission.lower()]

            sendMessage(player.phone, "Vous ne pouvez pas utiliser cette commande car vous n'êtes pas " + perm + " !", {"quotedMessageId": message.get("id")})
            return True
        elif game.pause and not is_necessary:
            sendMessage(player.phone, "La partie est actuellement en pause. Vous ne pouvez pas faire de commandes", {"quotedMessageId": message.get("id")})
            return True
        elif game.end and not is_necessary:
            sendMessage(player.phone, "La partie est actuellement terminée. Vous ne pouvez plus faire de commandes", {"quotedMessageId": message.get("id")})
        elif game.meeting and self.name not in ["help", "sos", "vote"]:
            sendMessage(player.phone, "Une réunion est en cours. Vous ne pouvez pas faire de commandes", {"quotedMessageId": message.get("id")})
            return True
        else:
            self.execute(player, content, message, game)
            return True

    def execute(self, player, content: str, message, game):
        """
        Exécute la commande
        :param player: Le joueur qui a effecuté la commande
        :param content: str: Le string envoyé par le message
        :param message: dict: Le message envoyé
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

    def execute(self, player, content: str, message, game) -> None:
        """
        Commande permettant d'avoir plus d'informations sur la tâche à effectuer
        :param player: Le joueur qui a exécuté la commande
        :param content: str: Le message envoyé par le joueur
        :param message: dict: Le message Whatsapp reçu
        :param game: La partie
        """
        try:
            task_number = int(content.split(" ")[1])
            task = player.tasks[task_number - 1]
            string = f"{task.name}\n"
            string += f"Lieu: {task.location}\n"
            string += f"Description: {task.description}\n"

            if "activ" in task.type:
                string += "Activée: "
                string += "Oui" if task.active else "Non"
                string += "\n"
            if task.done:
                "Tâche terminée !\n"
            sendMessage(player.phone, string, {"quotedMessageId": message.get("id")})
        except (Exception,):
            sendMessage(player.phone, "Veuillez entrer un numéro de tâche valide !", {"quotedMessageId": message.get("id")})


commands.append(TaskCommand())


class InfoCommand(Command):
    """
    Affiche les informations sur les tâches restantes
    """

    def __init__(self):
        super().__init__("info", "Permet de voir les tâches restantes", ["restant", "last", "reste"], "info", "info")

    def execute(self, player, content: str, message, game) -> None:
        """
        Commande permettant d'avoir plus d'informations sur la tâche à effectuer
        :param player: Le joueur qui a exécuté la commande
        :param content: str: Le message envoyé par le joueur
        :param message: dict: Le message Whatsapp reçu
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
                string += f"{i + 1}: {task.name} ({task.steps} étapes)\n"
        string = f"Il vous reste {remining} tâches à accomplir.\n" + string
        if done == len(player.tasks):
            string += "Vous avez accompli toutes vos tâches !\n"

        string += f"Il reste {len(game.done_tasks)}/{game.given_tasks} tâche pour les {game.config['names']['crewmate']}."

        string += f"\nVotre identifiant est {player.id}."
        sendMessage(player.phone, string, {"quotedMessageId": message.get("id")})


commands.append(InfoCommand())


class DeadsCommand(Command):
    """
    Affiche pour chaque joueur si jamais il est en vie ou non
    """

    def __init__(self):
        super().__init__("deads", "Voir les états de chaque joueur", ["view", "states", "états", "morts"], "deads",
                         "deads",
                         "scientist")

    def execute(self, player, content: str, message, game) -> None:
        """
        Commande qui renvoie l'état des personnes pour le rôle "Scientifique"
        :param player: Le joueur qui a exécuté la commande
        :param content: str: Le message envoyé par le joueur
        :param message: dict: Le message Whatsapp reçu
        :param game: La partie
        """
        if player.asks >= game.config["max_dead_check"]:
            sendMessage(player.phone, "Vous avez utilisé toutes vos demandes !", {"quotedMessageId": message.get("id")})
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
            sendMessage(player.phone, states, {"quotedMessageId": message.get("id")})


commands.append(DeadsCommand())


class MortCommand(Command):
    """
    Acte comme le signalement d'un cadavre par la personne
    """

    def __init__(self):
        super().__init__("mort", "Annonce à l'organisateur la découverte d'un corps", ["death", "cadavre", "corps"],
                         "mort PERSONNE", "mort 1")

    def execute(self, player, content: str, message, game) -> None:
        """
        Commande pour signaler une personne morte
        :param player: Le joueur qui a exécuté la commande
        :param content: str: Le message envoyé par le joueur
        :param message: dict: Le message Whatsapp reçu
        :param game: La partie
        """
        if game.game_master:
            response = messagebox.askokcancel("Mort détecté",
                                              f"{player.name} {player.lastname} découvert un corps ! Son message est :\n {content}")

            if response == "ok":
                game.start_meeting(f"Un cadavre a été signalé par {player.get_name()}.")
            elif response == "cancel":
                sendMessage(player.phone, "Votre demande a été refusée par l'organisateur.ice", {"quotedMessageId": message.get("id")})
        else:
            try:
                dead = parse_player(content, game)
                if not dead.dead:
                    sendMessage(player.phone, "Ce joueur ne peux pas être déclaré comme cadavre car il n'est pas mort", {"quotedMessageId": message.get("id")})
                else:
                    game.start_meeting(f"Un cadavre a été signalé par {player.get_name()}.")
            except (Exception,):
                sendMessage(player.phone, "Veuillez entrer un joueur valide !", {"quotedMessageId": message.get("id")})


commands.append(MortCommand())


class DoneCommand(Command):
    """
    Valide une tâche comme effectuée
    """

    def __init__(self):
        super().__init__("done", "Valide une tâche comme faite", ["fait", "réalisé"], "done NOMBRE", "done 1")

    def execute(self, player, content: str, message, game) -> None:
        """
        Commande pour déclarer qu'une tâche a été effectuée
        :param player: Le joueur qui a exécuté la commande
        :param content: str: Le message envoyé par le joueur
        :param message: dict: Le message Whatsapp reçu
        :param game: La partie
        """
        if player.role == "impostor":
            return sendMessage(player.phone, "Vous ne pouvez pas valider des tâches, vous êtes " + game.config["names"][
                "impostor"] + ".", {"quotedMessageId": message.get("id")})
        try:
            task_number = int(content.split(" ")[1])
            task = player.tasks[task_number - 1]
            if task.done:
                sendMessage(player.phone, "Vous avez déjà déclaré avoir fait la tâche " + str(task_number), {"quotedMessageId": message.get("id")})
            elif "valid" in task.type:
                sendMessage(player.phone,
                            "Vous ne pouvez pas déclarer avoir fait la tâche " + str(task_number) + " par une commande", {"quotedMessageId": message.get("id")})
            elif task.type == "activate_basic" and not task.active:
                sendMessage(player.phone, "Vous ne pouvez pas déclarer avoir fait la tâche " + str(
                    task_number) + " car elle n'est pas encore active", {"quotedMessageId": message.get("id")})
            else:
                game.task_done(player, task)
                sendMessage(player.phone, f"Votre tâche {task.name} a été confirmée comme faite !", {"quotedMessageId": message.get("id")})
        except Exception as e:
            print(e)
            sendMessage(player.phone, "Veuillez entrer un numéro de tâche valide !", {"quotedMessageId": message.get("id")})


commands.append(DoneCommand())


class HelpCommand(Command):
    """
    Affiche la page d'aide pour toutes les commandes ou pour une commande spécifique
    """

    def __init__(self):
        super().__init__("help", "Obtenir toutes les commandes et de l'aide pour chacune",
                         ["aide", "commandes", "commande", "commands", "command"], "help (COMMANDE)", "help help")

    def execute(self, player, content: str, message, game) -> None:
        """
        Commande qui renvoie toutes les commandes disponibles
        :param player: Le joueur qui a exécuté la commande
        :param content: str: Le message envoyé par le joueur
        :param message: dict: Le message Whatsapp reçu
        :param game: La partie
        """
        if len(content.split(" ")) == 1:
            string = "Voici toutes les commandes disponibles:\n"
            for command in commands:
                string += command.usage + ": " + command.description + "\n"
            sendMessage(player.phone, string, {"quotedMessageId": message.get("id")})
        else:
            command_str = content.split(" ")[1]
            command = None
            for cmd in commands:
                if command_str in ([cmd.name] + cmd.aliases):
                    command = cmd
                    break
            string = command.get_help(game.config)
            sendMessage(player.phone, string, {"quotedMessageId": message.get("id")})


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

    def execute(self, player, content: str, message, game) -> None:
        """
        Commande qui demande de l'aide aux autres joueurs
        :param player: Le joueur qui a exécuté la commande
        :param content: str: Le message envoyé par le joueur
        :param message: dict: Le message Whatsapp reçu
        :param game: La partie
        """
        game.send_info_all(
            f"{player.name} {player.lastname} a besoin d'aide en URGENCE ! Son message:\n{' '.join(content.split(' ')[1:])}")
        game.pause = True
        game.pause_reason = ' '.join(content.split(' ')[1:])
        code = game.set_pause_game()
        sendMessage(player.phone,
                    f"Votre demande d'aide a bien été transmise aux autres joueurs. Le code pour rétablir la partie normalement est '{code}'", {"quotedMessageId": message.get("id")})
        if game.game_master:
            messagebox.showerror(f"{player.name} {player.lastname} a besoin d'aide",
                                 f"{player.name} {player.lastname} a demandé de l'aide en URGENCE avec la commande SOS. Son message:\n{' '.join(content.split(' ')[1:])}\n\nUn message a été envoyé à tous les joueurs pour aller l'aider et la partie a été mise en pause")


commands.append(SOSCommand())


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

    def execute(self, player, content: str, message, game):
        """
        Tuer une personne
        :param player: Le joueur qui a exécuté la commande
        :param content: str: Le message envoyé par le joueur
        :param message: dict: Le message Whatsapp reçu
        :param game: La partie
        """
        player_id = re.match(r"\d{3}", content.split(" ")[1])
        if kills_cooldown.get(player.id):
            sendMessage(player.phone, "Vous ne pouvez pas tuer tout de suite", {"quotedMessageId": message.get("id")})
            return
        to_kill_player = None
        for joueur in game.players:
            if joueur.id == player_id[0]:
                to_kill_player = joueur
        if to_kill_player:
            if to_kill_player.id == player.id:
                sendMessage(player.phone, "Vous ne pouvez pas vous tuer vous-même", {"quotedMessageId": message.get("id")})
                return
            else:
                game.kill_player(to_kill_player)
                sendMessage(player.phone,
                            f"Le joueur {to_kill_player.name} {to_kill_player.lastname} a bien été tué de votre part !", {"quotedMessageId": message.get("id")})
                kills_cooldown[player.id] = True
                time.sleep(game.config["kill_cooldown"])
                del kills_cooldown[player.id]
        else:
            sendMessage(player.phone,
                        "Ce joueur n'a pas été trouvé ?! Merci de vérifier que la personne a bien donné son matricule.", {"quotedMessageId": message.get("id")})


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

    def execute(self, player, content: str, message, game):
        """
        Voter pour une personne
        :param player: Le joueur qui a exécuté la commande
        :param content: str: Le message envoyé par le joueur
        :param message: dict: Le message Whatsapp reçu
        :param game: La partie
        """
        if game.meeting != "vote":
            sendMessage(player.phone, "Il n'y a pas de période de vote en cours !", {"quotedMessageId": message.get("id")})
            return
        else:
            if player.id in game.meeting_votes.keys():
                sendMessage(player.phone, "Vous avez déjà voté !", {"quotedMessageId": message.get("id")})
                return
            else:
                if content.split(" ")[1] == "0" or content.split(" ")[1] == "skip" or content.split(" ")[1] == "passer":
                    game.meeting_votes[player.id] = "0"
                    sendMessage(player.phone, "Vous avez voté pour passer !", {"quotedMessageId": message.get("id")})
                    return
                voted_player: list = parse_player(content, game)
                if len(voted_player) > 1:
                    players_str = ""
                    for i, player in enumerate(voted_player):
                        players_str += f"{i + 1} - {player.name} {player.lastname}\n"
                    sendMessage(player.phone,
                                f"Plusieurs joueurs ont été trouvés:\n{players_str}Veuillez réessayer en précisant le numéro du joueur:\nvote NUMERO", {"quotedMessageId": message.get("id")})
                    return
                elif voted_player is None or len(voted_player) == 0:
                    sendMessage(player.phone, "Aucun joueur n'a été trouvé avec ce nom !", {"quotedMessageId": message.get("id")})
                    return
                else:
                    voted_player = voted_player[0]
                    game.meeting_votes[player.id] = voted_player.id
                    sendMessage(player.phone, f"Vous avez voté contre {voted_player.name} {voted_player.lastname} !", {"quotedMessageId": message.get("id")})
                    game.timer.show_players()
                    return


commands.append(VoteCommand())


def parse_player(content: str, game) -> list:
    """
    Trouve un joueur donné un argument dans une commande
    :param content: str: Le message envoyé par le joueur
    :param game: La partie
    :return SMSPlayer or None or str: Le joueur si trouvé
    """
    try:
        player_id = int(content.split(" ")[1])
        player = game.players[player_id - 1]
        return [player]
    except (Exception,):
        player_name = content.split(" ")[1].lower()
        found_players = []
        for i in range(game.players):
            player = game.players[i]
            if player.name.lower() == player_name or player.lastname.lower() == player_name:
                player_with_id = (i + 1, player)
                found_players.append(player_with_id)

        return found_players
