#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import time
from tkinter import *
from tkinter import messagebox

from discord import app_commands

from classes import DiscordPlayer
from game_class import Game
import json
import random
from discord_us.commands import commands, autocomplete
import discord
from discord.ext import commands as dcommands
import requests
import os
from utils import clear_frame, VerticalScrolledFrame
from threading import Thread

url = "https://discord.com/api/v10/applications/{app_id}/commands"


class DiscordClient(discord.Client):
    def __init__(self, *, intents: discord.Intents, game):
        super().__init__(
            intents=intents,
            command_prefix="us.",
        )
        self.tree = app_commands.CommandTree(self)
        self.game = game
        basic_tree_error = self.tree.on_error

        async def tree_error(interaction: discord.Interaction[app_commands], error: app_commands.AppCommandError):
            if isinstance(error, app_commands.CommandNotFound):
                return
            await basic_tree_error(interaction, error)

        self.tree.on_error = tree_error

    def export_commands(self):
        slash_commands = [c.export_slash() for c in commands]
        headers = {
            "Authorization": f"Bot {self.game.config['discord_token']}"
        }
        r = requests.put(url.replace("{app_id}", str(self.user.id)), json=slash_commands, headers=headers)
        if r.status_code != 200:
            print(r.text)
        else:
            print("Commands exported")

    async def on_ready(self):
        await self.change_presence(activity=discord.Game(name="Gère une partie d'among us"),
                                   status=discord.Status.online)
        self.export_commands()
        print("Bot is ready")


class DiscordGame(Game):
    def __init__(self, game_master: bool = None):
        self.send_messages = []
        intents = discord.Intents.all()
        self.client = client = DiscordClient(intents=intents, game=self)

        with open("config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)

        @client.event
        async def on_interaction(interaction: discord.Interaction):
            if interaction.type == discord.InteractionType.application_command:
                command = next((c for c in commands if c.name == interaction.data["name"]), None)
                player = self.get_player_from_discord(interaction.user)
                if command is not None:
                    try:
                        await command.run(player, interaction, self)
                    except Exception as e:
                        print(e)
                        is_in_guild = interaction.guild_id is not None
                        await interaction.response.send_message("Une erreur est survenue", ephemeral=is_in_guild)
                else:
                    is_in_guild = interaction.guild_id is not None
                    await interaction.response.send_message("Commande non trouvée", ephemeral=is_in_guild)
            elif interaction.type == discord.InteractionType.autocomplete:
                await autocomplete(interaction, self)
            else:
                interaction.response.send_message("Type d'interaction non reconnu")

        @client.event
        async def on_message(message: discord.Message):
            if message.author == self.client.user:
                return
            if message.channel.type == discord.ChannelType.private:
                player = self.get_player_from_discord(message.author)
                if self.import_window is not None:
                    if self.register_code in message.content:
                        if player is None:
                            new_player = {
                                "type": "discord",
                                "name": message.author.display_name,
                                "username": message.author.name,
                                "id": message.author.id,
                            }
                            player = DiscordPlayer(message.author.display_name, message.author.name, message.author.id,
                                                   self.used_passwords,
                                                   self.used_id)
                            self.players.append(player)
                            if self.config["save_register"]:
                                players = []
                                if os.path.exists("players.json"):
                                    with open("players.json", "r", encoding="utf-8") as file:
                                        players = json.load(file)
                                players.append(new_player)
                                with open("players.json", "w", encoding="utf-8") as file:
                                    json.dump(players, file, indent=4, ensure_ascii=False)
                            await message.reply(content="Vous êtes bien enregistré dans la partie !")
                            self.import_players()
                        else:
                            await message.reply(content="Vous êtes déjà enregistré dans la partie !")
                if player is not None:
                    content = message.content.lower()
                    if self.unpause_code in content and self.pause:
                        self.unpause_self()
                        return True
                    for task in player.tasks:
                        if task.type == "validate_basic":
                            for word in task.keywords:
                                if word in content:
                                    self.task_done(player, task)
                                    break
                        elif task.type == "activate_basic":
                            for word in task.activ_keywords:
                                if word in content:
                                    await message.reply(content=f"La tâche {task.name} vous envoie:\n{task.message}")
                                    task.active = True
                                    break
                        elif task.type == "activ_valid":
                            for word in task.keywords:
                                if word in content:
                                    if task.active:
                                        self.task_done(player, task)
                                        await message.reply(content="Vous avez bien validé la tâche !")
                                        break
                                    else:
                                        await message.reply(content="La tâche n'est pas encore activée")
                                        break
                            for word in task.activ_keywords:
                                if word in content:
                                    await message.reply(content=f"La tâche {task.name} vous envoie:\n{task.message}")
                                    task.active = True
                                    break
                        else:
                            string = "Nouveau message de " + player.get_name() + " (" + player.username + ") :\n"
                            string += message.content
                            messagebox.showinfo(f"Message de {message.author.display_name}", string, parent=self.window)

        self.flt = flt = Thread(target=lambda: client.run(self.config["discord_token"]))
        flt.daemon = True
        flt.start()
        time.sleep(5)
        super().__init__(game_master)

    def import_players(self):
        if self.config["register_type"] == "liste":
            used_passwords: list = []
            used_id: list = []
            with open("players.json", "r", encoding='utf-8') as f:
                data = json.load(f)
                self.players = [DiscordPlayer(player["name"], player["username"], player["id"], used_passwords, used_id)
                                for player in data if
                                player.get("play", True) and player.get("type", "") == "discord"]

                self.start_game()
        else:
            already_started: bool = self.import_window is not None
            if self.import_window:
                clear_frame(self.import_window)
                popup = self.import_window
            else:
                self.import_window = popup = Tk()
                popup.title("Importation des joueurs")
                popup.geometry("300x200")
                popup.resizable(True, True)
                popup.iconbitmap(self.path + "/assets/img/amongus.ico")
                popup.state("zoomed")
                self.register_code = "".join([str(random.randint(0, 9)) for _ in range(5)])

            def start_game() -> None:
                """
                Démarre la partie, une fois que les joueurs sont importés
                :return: None
                """
                self.import_window = None
                self.players = [player for player in self.players if player is not None]
                popup.destroy()
                self.register_code = None
                self.start_game()
                return None

            def closing():
                """
                Fonction de fermeture de la fenêtre
                """
                if messagebox.askokcancel("Quitter", "Êtes vous sûr de quitter ?", parent=self.window):
                    popup.destroy()
                    self.receive = False
                    self.window.destroy()

            popup.protocol("WM_DELETE_WINDOW", closing)

            main_frame = Frame(popup)

            qrcode_frame = Frame(main_frame)

            name = self.client.user.global_name
            if self.client.user.discriminator:
                name += "(" + self.client.user.name + "#" + self.client.user.discriminator + ")"
            else:
                name += "(" + self.client.user.name + ")"

            url_label = Label(qrcode_frame,
                              text=f"Envoyez {self.register_code} à {name} pour vous enregistrer",
                              font=("Arial", 28))
            url_label.pack()

            qrcode_frame.pack(fill=BOTH, expand=True)

            valid_players = [player for player in self.players if player is not None]

            start_button = Button(main_frame, text="Démarrer la partie", command=start_game)

            if len(valid_players) < 4:
                start_button.config(state=DISABLED)

            start_button.pack()

            import_players_frame = VerticalScrolledFrame(main_frame)

            for player in valid_players:
                player_frame = Frame(import_players_frame)

                player_label = Label(player_frame, text=player.get_name(), font=("Arial", 28))
                player_label.pack()

                player_frame.pack(fill=BOTH, expand=True)

            import_players_frame.pack(fill=BOTH, expand=True)

            main_frame.pack(fill=BOTH, expand=True)

            if not already_started:
                popup.mainloop()
        print("Joueurs importés")

    def send_info_all(self, message: str):
        print("Envoie de l'information")
        for player in self.players:
            new_message = message.replace("{name}", player.display_name)
            # replace the variable in the message
            new_message = new_message.replace("{role}", self.config["names"][player.role])
            new_message = new_message.replace("{id}", player.id)
            new_message = new_message.replace("{username}", player.username)
            new_message = new_message.replace("{tasks}", "\n".join([task.name for task in player.tasks]))
            new_message = new_message.replace("{password}", player.password)

            print(player.display_name, ":", new_message)

            async def execute(joueur, msg):
                user = await self.client.fetch_user(joueur.discord_id)
                if user is None:
                    print("User really not found")
                else:
                    await user.send(content=msg)

            asyncio.run_coroutine_threadsafe(execute(player, new_message), self.client.loop)

    def send_info(self, player: DiscordPlayer, message: str):
        print(player.display_name, ":", message)

        async def execute():
            user = await self.client.fetch_user(player.discord_id)
            if user is None:
                print("User really not found")
            else:
                await user.send(content=message)

        asyncio.run_coroutine_threadsafe(execute(), self.client.loop)

    def send_role(self, player: DiscordPlayer) -> None:
        """
        Envoie un sms au joueur indiquant son role et ses tâches
        :param player: DiscordPlayer: Le joueur
        """
        message = f"Bonjour {player.get_name()},\n"
        message += "Vous êtes un " + self.config["names"][player.role].upper()
        if player.role == "impostor" and len(self.impostors) > 1:
            impostors = " ".join([(joueur.get_name()) for joueur in self.impostors])
            message += " avec " + impostors + "\n\n"
        else:
            message += "\n\n"
        message += "Vos tâches sont:\n"
        for i in range(len(player.tasks)):
            task = player.tasks[i]
            message += f"{i + 1}: {task.name} ({task.steps} étapes)\n"
        message += "\n"
        message += f"Votre identifiant est {player.id}\n"
        message += "\n"
        message += "Pour voir toutes les commandes, vous pouvez taper \"help\"\n"
        message += "Nous vous souhaitons une bonne partie !"

        self.send_info(player, message)

    def get_discord_user(self, user_id: str) -> discord.User:
        return next((user for user in self.client.users if str(user.id) == str(user_id)), None)

    def get_player_from_discord(self, user: discord.User) -> DiscordPlayer:
        return next((player for player in self.players if str(player.discord_id) == str(user.id)), None)

    def end_game(self):
        """
        Termine la partie
        :return:
        """
        self.window.destroy()
        asyncio.run_coroutine_threadsafe(self.client.close(), self.client.loop)


if __name__ == '__main__':
    DiscordGame(True)
