#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import messagebox, ttk
from classes import InstaPlayer
from game_class import Game
import json
import random
from instagram.commands import commands
from instagram.instagram_manager import send_message, get_new_messages
from flask import Flask, request
from threading import Thread
import os


class InstagramGame(Game):
    def __init__(self, game_master: bool = None):
        self.receive = True
        self.send_messages = []
        Timer(1, self.start_recieve_sms).start()

        super().__init__()

    def import_players(self):
        if self.config["register_type"] == "liste": 
            used_passwords: list = []
            used_id: list = []
            with open("players.json", "r", encoding='utf-8') as f:
                data = json.load(f)
                self.players = [InstaPlayer(player["name"], player["username"], used_passwords, used_id)
                                for player in data if player.get("play", True) and player.get("type", "") == "instagram"]
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
                if messagebox.askokcancel("Quitter", "Êtes vous sûr de quitter ?"):
                    popup.destroy()
                    self.window.destroy()
    
            popup.protocol("WM_DELETE_WINDOW", closing)
    
            main_frame = Frame(popup)
    
            qrcode_frame = Frame(main_frame)
    
            url_label = Label(qrcode_frame, text=f"Envoyez {self.register_code} à {self.config["insta_user"]} pour vous enregistrer", font=("Arial", 28))
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
            new_message = message.replace("{name}", player.name)
            # replace the variable in the message
            new_message = new_message.replace("{role}", self.config["names"][player.role])
            new_message = new_message.replace("{id}", player.id)
            new_message = new_message.replace("{username}", player.username)
            new_message = new_message.replace("{tasks}", "\n".join([task.name for task in player.tasks]))
            new_message = new_message.replace("{password}", player.password)

            print(player.name, ":", new_message)
            send_message(player.username, new_message)

    def send_info(self, player: InstaPlayer, message: str):
        print(player.name, ":", message)
        send_message(player.username, message)

    def send_role(self, player: InstaPlayer) -> None:
        """
        Envoie un sms au joueur indiquant son role et ses tâches
        :param player: InstaPlayer: Le joueur
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

        self.send_messages.append(message)
        self.send_info(player, message)

    def check_command(self, player, message: dict) -> bool:
        """
        Vérifie si jamais le content reçu est une commande ou un content validant une tâche. Si c’est le cas, on l'exécute
        :param player: SMSPlayer: Le joueur qui a envoyé le content
        :param message: str: le contenu du content reçu
        :return: bool: Si jamais le content était bien une commande
        """
        content = message["body"].lower()
        for cmd in commands:
            if content.startswith(tuple([cmd.name] + cmd.aliases)):
                return cmd.run(player, content, message, self)
        if self.unpause_code in content and self.pause:
            self.unpause_game()
            return True
        for task in player.tasks:
            if task.type == "validate_basic":
                for word in task.keywords:
                    if word in content:
                        self.task_done(player, task)
                        return True
            elif task.type == "activate_basic":
                for word in task.activ_keywords:
                    if word in content:
                        send_message(player.username, f"La tâche {task.name} vous envoie:\n{task.message}")
                        task.active = True
                        return True
            elif task.type == "activ_valid":
                for word in task.keywords:
                    if word in content:
                        if task.active:
                            self.task_done(player, task)
                            send_message(player.username, "Vous avez bien validé la tâche !")
                            return True
                        else:
                            send_message(player.username, "La tâche n'est pas encore activée")
                            return True
                for word in task.activ_keywords:
                    if word in content:
                        send_message(player.username, f"La tâche {task.name} vous envoie:\n{task.message}")
                        task.active = True
                        return True

        return False
    
    def start_recieve_message(self):
        """
        Active la vérification périodique de la réception de SMS
        """

        def recieve():
            try:
                new = get_new_messages()
            except Exception as e:
                print(e)
                new = []
            if len(new) > 0:
                for msg in new:
                    joueur = next((joueur for joueur in self.players if joueur.username == msg["username"]), None)
                    if self.import_window is not None:
                        if self.register_code in msg["text"]:
                            if joueur is not None:
                                return self.send_info(joueur, "Vous êtes déjà enregistré dans la partie !")
                            new_player = {
                                "type": "instagram"
                                "name": msg["full_name"], 
                                "username": msg["username"]
                            }
                            player = InstaPlayer(new_player["name"], new_player["username"], self.used_passwords, self.used_id)
                            self.players.append(player)
                            if self.config["save_register"]:
                                
                                players = []
                                if os.path.exists("players.json"):
                                    with open("players.json", "r", encoding="utf-8") as file:
                                        players = json.load(file)
                                players.append(new_player)
                                with open("players.json", "w", encoding="utf-8") as file:
                                    json.dump(players, file, indent=4, ensure_ascii=False)
                            self.send_info(player, "Vous êtes bien entré dans la partie !")
                            self.import_players()
                            continue
                    if self.check_command(joueur, msg.content):
                        continue
                    string = "Nouveau message de " + joueur.get_name() + " (" + joueur.username + ") :\n"
                    string += msg.content
                    messagebox.showinfo(f"Message de {msg.username}", string)
                if self.receive:
                    Timer(5, recieve).start()

        Timer(2, recieve).start()


if __name__ == '__main__':
    InstaGame(True)
