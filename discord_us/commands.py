import asyncio
import time
from tkinter import messagebox
import re  # Importation du module pour faire des tests d'expressions régulières
import discord
from discord import ext, app_commands

kills_cooldown = {}


def is_guild(interaction: discord.Interaction) -> bool:
    """
    Vérifie si l'interaction est dans un serveur
    :param interaction: discord.Interaction: L'interaction
    :return: bool: Si l'interaction est dans un serveur
    """
    return interaction.guild is not None


class Command:
    """
    Initialisation de la classe commande
    """

    def __init__(self,
                 name: str,
                 description: str,
                 options: list,
                 usage: str,
                 exemple: str,
                 permission: str = None):
        self.name: str = name
        self.description: str = description
        self.options: list = options
        self.usage: str = usage
        self.exemple: str = exemple
        self.permission: str = permission


    def export_slash(self):
        """
        Exporte la commande en slash command
        """
        return {
            "type": discord.AppCommandType.chat_input.value,
            "name": self.name,
            "description": self.description,
            "options": self.options,
            "dm_permission": True
        }

    def get_help(self, config: dict = None) -> str:
        """
        Affiche la page d'aide pour la commande
        :param config: dict: la configuration du jeu
        :return: str: Le string avec l'aide de la commande
        """
        string: str = "Voici la page d'aide pour la commande " + self.name + ":"
        string += "\n" + self.description
        if self.permission:
            string += "\nUtilisable par: "
            if config is not None and config.get("names") and config["names"].get(self.permission.lower()):
                string += config["names"][self.permission.lower()]
            else:
                string += self.permission
        string += "\nUtilisation: " + self.usage + " (exemple: " + self.exemple + ")"
        return string

    async def run(self, player, interaction: discord.Interaction, game) -> bool:
        """
        Exécute la commande avec une vérification du rôle et de la partie
        :param player: Le joueur qui a effecuté la commande
        :param interaction: discord.Interaction: Le string envoyé par le message
        :param game: La partie
        :return: bool: Renvoie la bonne utilisation de la commande
        """
        is_gui = is_guild(interaction)
        is_necessary = self.name in ["help", "sos"]
        # Check permission
        if self.permission and player.role != self.permission:
            perm: str = self.permission
            if game.config.get("names") and game.config["names"].get(self.permission.lower()):
                perm = game.config["names"][self.permission.lower()]

            await interaction.response.send_message(content=
                                                    "Vous ne pouvez pas utiliser cette commande car vous n'êtes pas " + perm + " !",
                                                    ephemeral=is_gui)
            return True
        elif game.pause and not is_necessary:
            await interaction.response.send_message(content=
                                                    "La partie est actuellement en pause. Vous ne pouvez pas faire de commandes",
                                                    ephemeral=is_gui)
            return True
        elif game.end and not is_necessary:
            await interaction.response.send_message(content=
                                                    "La partie est actuellement terminée. Vous ne pouvez plus faire de commandes",
                                                    ephemeral=is_gui)
        elif game.meeting and self.name not in ["help", "sos", "vote"]:
            await interaction.response.send_message(content=
                                                    "Une réunion est en cours. Vous ne pouvez pas faire de commandes",
                                                    ephemeral=is_gui)
            return True
        else:
            await self.execute(player, interaction, game)
            return True

    async def execute(self, player, interaction: discord.Interaction, game):
        """
        Exécute la commande
        :param player: Le joueur qui a effecuté la commande
        :param interaction: discord.Interaction: Le string envoyé par le message
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
                         [
                             {
                                 "type": discord.AppCommandOptionType.integer.value,
                                 "name": "task_id",
                                 "description": "Le numéro de la tâche",
                                 "required": True,
                                 "autocomplete": True
                             }
                         ],
                         "task NOMBRE", "task 1")

    async def execute(self, player, interaction: discord.Interaction, game) -> None:
        """
        Commande permettant d'avoir plus d'informations sur la tâche à effectuer
        :param player: Le joueur qui a exécuté la commande
        :param interaction: discord.Interaction: Le message envoyé par le joueur
        :param game: La partie
        """
        try:
            task_number = int(interaction.data["options"][0]["value"])
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
            await interaction.response.send_message(content=string, ephemeral=is_guild(interaction))
        except (Exception,):
            await interaction.response.send_message(content="Veuillez entrer un numéro de tâche valide !", ephemeral=is_guild(interaction))


commands.append(TaskCommand())


class InfoCommand(Command):
    """
    Affiche les informations sur les tâches restantes
    """

    def __init__(self):
        super().__init__("info",
                         "Permet de voir les tâches restantes",
                         [],
                         "info", "info")

    async def execute(self, player, interaction: discord.Interaction, game) -> None:
        """
        Commande permettant d'avoir plus d'informations sur la tâche à effectuer
        :param player: Le joueur qui a exécuté la commande
        :param interaction: discord.Interaction: Le message envoyé par le joueur
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
        await interaction.response.send_message(content=string, ephemeral=is_guild(interaction))


commands.append(InfoCommand())


class DeadsCommand(Command):
    """
    Affiche pour chaque joueur si jamais il est en vie ou non
    """

    def __init__(self):
        super().__init__("deads", "Voir les états de chaque joueur",
                         [],
                         "deads",
                         "deads",
                         "scientist")

    async def execute(self, player, interaction: discord.Interaction, game) -> None:
        """
        Commande qui renvoie l'état des personnes pour le rôle "Scientifique"
        :param player: Le joueur qui a exécuté la commande
        :param interaction: discord.Interaction: Le message envoyé par le joueur
        :param game: La partie
        """
        if player.asks >= game.config["max_dead_check"]:
            await interaction.response.send_message(content="Vous avez utilisé toutes vos demandes !", ephemeral=is_guild(interaction))
        else:
            states = "Voici les états de chaque joueur:\n"
            for joueur in game.players:
                if joueur.dead:
                    states += "- " + joueur.get_name() + " (mort)\n"
                else:
                    states += "- " + joueur.get_name() + " (vivant)\n"
            player.asks += 1
            states += "\n Il vous reste " + str(game.config["max_dead_check"] - player.asks) + "/" + str(
                game.config["max_dead_check"]) + " demandes."
            await interaction.response.send_message(content=states, ephemeral=is_guild(interaction))


commands.append(DeadsCommand())


class MortCommand(Command):
    """
    Acte comme le signalement d'un cadavre par la personne
    """

    def __init__(self):
        super().__init__("mort", "Annonce à l'organisateur la découverte d'un corps",
                         [
                             {
                                 "type": discord.AppCommandOptionType.string.value,
                                 "name": "player",
                                 "description": "Le joueur mort",
                                 "required": True
                             }
                         ],
                         "mort PERSONNE", "mort 1")

    async def execute(self, player, interaction: discord.Interaction, game) -> None:
        """
        Commande pour signaler une personne morte
        :param player: Le joueur qui a exécuté la commande
        :param interaction: discord.Interaction: Le message envoyé par le joueur
        :param game: La partie
        """
        dead_id = interaction.data["options"][0]["value"]
        dead = game.get_player(dead_id)
        if dead is None:
            await interaction.response.send_message(content=
                                                    "Ce joueur n'a pas été trouvé ?! Merci de vérifier que la personne a bien donné son matricule.",
                                                    ephemeral=is_guild(interaction))
            return
        if game.game_master:
            await interaction.response.defer()
            response = messagebox.askokcancel("Mort détecté",
                                              f"{player.get_name()} découvert le corps de {dead.get_name()}. Voulez-vous lancer une réunion ?",
                                              parent=game.window)

            if response == "ok":
                await interaction.edit_original_response(content="La demande a été acceptée par l'organisateur.ice", ephemeral=is_guild(interaction))
                game.start_meeting(f"Un cadavre a été signalé par {player.get_name()}.")
            elif response == "cancel":
                await interaction.edit_original_response(content="Votre demande a été refusée par l'organisateur.ice", ephemeral=is_guild(interaction))
        else:
            try:
                if not dead.dead:
                    await interaction.response.send_message(content=
                                                            "Ce joueur ne peut pas être déclaré comme cadavre car il n'est pas mort", ephemeral=is_guild(interaction))
                else:
                    game.start_meeting(f"Un cadavre a été signalé par {player.get_name()}.")
            except (Exception,):
                await interaction.response.send_message(content="Veuillez entrer un joueur valide !", ephemeral=is_guild(interaction))


commands.append(MortCommand())


class DoneCommand(Command):
    """
    Valide une tâche comme effectuée
    """

    def __init__(self):
        super().__init__("done", "Valide une tâche comme faite",
                         [{
                             "type": discord.AppCommandOptionType.integer.value,
                             "name": "task_id",
                             "description": "Le numéro de la tâche",
                             "required": True,
                             "autocomplete": True
                         }],
                         "done NOMBRE", "done 1")

    async def execute(self, player, interaction: discord.Interaction, game) -> None:
        """
        Commande pour déclarer qu'une tâche a été effectuée
        :param player: Le joueur qui a exécuté la commande
        :param interaction: discord.Interaction: Le message envoyé par le joueur
        :param game: La partie
        """
        if player.role == "impostor":
            return game.send_info(player,
                                  "Vous ne pouvez pas valider des tâches, vous êtes " + game.config["names"][
                                      "impostor"] + ".")
        try:
            task_number = int(interaction.data["options"][0]["value"])
            task = player.tasks[task_number - 1]
            if task.done:
                await interaction.response.send_message(content=
                                                        "Vous avez déjà déclaré avoir fait la tâche " + str(
                                                            task_number), ephemeral=is_guild(interaction))
            elif "valid" in task.type:
                game.send_info(player,
                               "Vous ne pouvez pas déclarer avoir fait la tâche " + str(
                                   task_number) + " par une commande")
            elif task.type == "activate_basic" and not task.active:
                await interaction.response.send_message(content=
                                                        "Vous ne pouvez pas déclarer avoir fait la tâche " + str(
                                                            task_number) + " car elle n'est pas encore active", ephemeral=is_guild(interaction))
            else:
                await interaction.response.defer()
                game.task_done(player, task)
                await interaction.edit_original_response(content=
                                                        f"Votre tâche {task.name} a été confirmée comme faite !", ephemeral=is_guild(interaction))
        except Exception as e:
            print(e)
            await interaction.response.send_message(content=
                                                    "Veuillez entrer un numéro de tâche valide !", ephemeral=is_guild(interaction))


commands.append(DoneCommand())


class HelpCommand(Command):
    """
    Affiche la page d'aide pour toutes les commandes ou pour une commande spécifique
    """

    def __init__(self):
        super().__init__("help", "Obtenir toutes les commandes et de l'aide pour chacune",
                         [
                             {
                                 "type": discord.AppCommandOptionType.integer.value,
                                 "name": "command",
                                 "description": "La commande pour laquelle obtenir de l'aide",
                                 "required": False
                             }
                         ],
                         "help (COMMANDE)", "help help")

    async def execute(self, player, interaction: discord.Interaction, game) -> None:
        """
        Commande qui renvoie toutes les commandes disponibles
        :param player: Le joueur qui a exécuté la commande
        :param interaction: discord.Interaction: Le message envoyé par le joueur
        :param game: La partie
        """
        if len(interaction.data.get("options", [])) == 0:
            string = "Voici toutes les commandes disponibles:\n"
            for command in commands:
                string += command.usage + ": " + command.description + "\n"
            await interaction.response.send_message(content=string, ephemeral=is_guild(interaction))
        else:
            command_str = interaction.data["options"][0]["value"]
            command = None
            for cmd in commands:
                if command_str in ([cmd.name] + cmd.aliases):
                    command = cmd
                    break
            string = command.get_help(game.config)
            await interaction.response.send_message(content=string, ephemeral=is_guild(interaction))


commands.append(HelpCommand())


class SOSCommand(Command):
    """
    Permet aux joueurs de demander de l'aide aux autres joueurs en cas de problèmes urgent
    """

    def __init__(self):
        super().__init__(
            "sos",
            "Commande d'URGENCE pour signaler que vous avez un problème",
            [
                {
                    "type": discord.AppCommandOptionType.integer.value,
                    "name": "message",
                    "description": "Le message à envoyer, incluant la localisation",
                    "required": False
                }
            ],
            "sos (LOCALISATION - MESSAGE)",
            "sos maison problème de jambe")

    async def execute(self, player, interaction: discord.Interaction, game) -> None:
        """
        Commande qui demande de l'aide aux autres joueurs
        :param player: Le joueur qui a exécuté la commande
        :param interaction: discord.Interaction: Le message envoyé par le joueur
        :param game: La partie
        """
        message = interaction.data.get("options", ["None"])[0]["value"]
        game.send_info_all(
            f"{player.get_name()} a besoin d'aide en URGENCE ! Son message:\n{message}")
        game.pause = True
        game.pause_reason = message
        code = game.set_pause_game()
        await interaction.response.send_message(
            content=f"Votre demande d'aide a bien été transmise aux autres joueurs. Le code pour rétablir la partie normalement est '{code}'", ephemeral=is_guild(interaction))
        if game.game_master:
            messagebox.showerror(f"{player.get_name()} a besoin d'aide",
                                 f"{player.get_name()} a demandé de l'aide en URGENCE avec la commande SOS. Son message:\n{message}\n\nUn message a été envoyé à tous les joueurs pour aller l'aider et la partie a été mise en pause",
                                 parent=game.window)


commands.append(SOSCommand())


class KillCommand(Command):
    """
    Permet aux imposteurs de tuer une personne
    """

    def __init__(self):
        super().__init__(
            "kill",
            "Tuer une personne, si elle est à côté de vous",
            [
                {
                    "type": discord.AppCommandOptionType.string.value,
                    "name": "player",
                    "description": "Le joueur à tuer",
                    "required": True,
                    "max_length": 3,
                    "min_length": 3,
                }
            ],
            "kill PERSONNE",
            "kill Merlode",
            "impostor"
        )

    async def execute(self, player, interaction: discord.Interaction, game):
        """
        Tuer une personne
        :param player: Le joueur qui a exécuté la commande
        :param interaction: discord.Interaction: Le message envoyé par le joueur
        :param game: La partie
        """
        player_id = interaction.data["options"][0]["value"]
        if kills_cooldown.get(player.id):
            await interaction.response.send_message(content=
                                                    "Vous ne pouvez pas tuer tout de suite", ephemeral=is_guild(interaction))
            return
        to_kill_player = game.get_player(player_id)
        if to_kill_player:
            if to_kill_player.id == player.id:
                await interaction.response.send_message(content=
                                                        "Vous ne pouvez pas vous tuer vous-même", ephemeral=is_guild(interaction))
                return
            else:
                await interaction.response.defer()
                game.kill_player(to_kill_player)
                await interaction.edit_original_response(content=
                                                        f"Le joueur {to_kill_player.get_name()} a bien été tué de votre part !", ephemeral=is_guild(interaction))
                kills_cooldown[player.id] = True
                await asyncio.sleep(10)
                del kills_cooldown[player.id]
        else:
            await interaction.response.send_message(content=
                                                    "Ce joueur n'a pas été trouvé ?! Merci de vérifier que la personne a bien donné son matricule.", ephemeral=is_guild(interaction))


commands.append(KillCommand())


class VoteCommand(Command):
    def __init__(self):
        super(VoteCommand, self).__init__(
            "vote",
            "Voter pour une personne durant les phases de meeting",
            [
                {
                    "type": discord.AppCommandOptionType.integer.value,
                    "name": "player",
                    "description": "Le joueur pour lequel voter",
                    "required": True,
                    "autocomplete": True
                }
            ],
            "vote PERSONNE",
            "vote 1"
        )

    async def execute(self, player, interaction: discord.Interaction, game):
        """
        Voter pour une personne
        :param player: Le joueur qui a exécuté la commande
        :param interaction: discord.Interaction: Le message envoyé par le joueur
        :param game: La partie
        """
        if game.meeting != "vote":
            await interaction.response.send_message(content=
                                                    "Il n'y a pas de période de vote en cours !", ephemeral=is_guild(interaction))
            return
        else:
            if player.id in game.meeting_votes.keys():
                await interaction.response.send_message(content=
                                                        "Vous avez déjà voté !", ephemeral=is_guild(interaction))
                return
            else:
                vote_id = interaction.data["options"][0]["value"]
                if vote_id == "0" or vote_id == "skip" or vote_id == "passer":
                    game.meeting_votes[player.id] = "0"
                    await interaction.response.send_message(content=
                                                            "Vous avez voté pour passer !", ephemeral=is_guild(interaction))
                    return
                try:
                    voted_player = game.players[vote_id]
                    game.meeting_votes[player.id] = voted_player.id
                    await interaction.response.send_message(content=
                                                            f"Vous avez voté contre {voted_player.get_name()} !", ephemeral=is_guild(interaction))
                    game.timer.show_players()
                except (Exception,):
                    await interaction.response.send_message(content=
                                                            "Aucun joueur n'a été trouvé avec ce nom !", ephemeral=is_guild(interaction))


commands.append(VoteCommand())


async def autocomplete(interaction: discord.Interaction, game) -> None:
    """
    Autocomplète les commandes
    :param interaction: discord.Interaction: Le message envoyé par le joueur
    :param game: La partie
    """

    def is_content_similar(content, value) -> bool:
        return value.lower() in content.lower()

    if interaction.data["name"] == "vote":
        if game.meeting != "vote":
            await interaction.response.autocomplete([app_commands.Choice(
                name="Erreur: Pas de vote en cours",
                value="None"
            )])
        value = interaction.data["options"][0]["value"]
        player = game.get_player_from_discord(interaction.user)

        def can_be_voted(i: int) -> bool:
            return not game.players[i].dead and game.players[
                i].id != player.id and value in f"{i + 1} - {game.players[i].get_name()}"

        choices = [app_commands.Choice(
            name=f"{i + 1} - {game.players[i].get_name()}",
            value=str(i)
        ) for i in range(len(game.players)) if
            can_be_voted(i) and is_content_similar(f"{i + 1} - {game.players[i].get_name()}", value)]
        choices.insert(0, app_commands.Choice(
            name="Passer",
            value="0"
        ))
        await interaction.response.autocomplete(choices)
    elif interaction.data["name"] == "task":
        value = interaction.data["options"][0]["value"]
        player = game.get_player_from_discord(interaction.user)
        choices = [app_commands.Choice(
            name=f"{i + 1} - {player.tasks[i].name}",
            value=str(i+1)
        ) for i in range(len(player.tasks)) if is_content_similar(f"{i + 1} - {player.tasks[i].name}", value)]
        await interaction.response.autocomplete(choices)
    elif interaction.data["name"] == "done":
        value = interaction.data["options"][0]["value"]
        player = game.get_player_from_discord(interaction.user)
        choices = [app_commands.Choice(
            name=f"{i + 1} - {player.tasks[i].name}",
            value=str(i+1)
        ) for i in range(len(player.tasks)) if is_content_similar(f"{i + 1} - {player.tasks[i].name}", value)]
        await interaction.response.autocomplete(choices)
