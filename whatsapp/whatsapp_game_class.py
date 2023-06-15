#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import messagebox, ttk
from classes import SMSPlayer, BasicTask
from game_class import Game
import json
import random
from whatsapp.commands import commands
from whatsapp.whatsapp_manager import sendMessage, isReady
import datetime
from threading import Timer
from flask import Flask, request
from threading import Thread
import pyqrcode
import os


class WhatsAppGame(Game):
    def __init__(self, game_master: bool = None):
        self.receive = True
        self.send_messages = []
        self.server = app = Flask(__name__)
        # Start the NodeJs process to manage the whatsapp connection and get the logs from the process in a thread
        self.whatsapp_manager = Thread(target=lambda: os.system("node whatsapp/api/index.js"))
        self.whatsapp_manager.start()

        self.isReady = False

        @app.post("/qr")
        def qr():
            print("Please scan the QR code below to authenticate.")
            return "OK", 200

        @app.post("/authenticated")
        def authenticated():
            return "OK", 200

        @app.post("/auth_failure")
        def auth_failure():
            return "OK", 200

        @app.post("/ready")
        def ready():
            print("WhatsApp is ready")
            messagebox.showinfo("Bienvenue", "Bienvenue dans le jeu " + self.config["names"]["title"] + "\n" +
                                "Une nouvelle partie va commencer.\n" +
                                "Êtes-vous prêt à jouer ?")
            self.start_game()
            return "OK", 200

        @app.post("/message")
        def message():
            data = request.json["data"]
            if len(data["from"]) > 16:
                return "OK", 200
            joueur = next((player for player in self.players if
                           player.phone.replace("+", "") == data["from"].replace("@c.us", "")), None)
            if not self.check_command(joueur, data):
                string = "Nouveau message de " + joueur.name + " " + joueur.lastname + " (" + joueur.phone + ") :\n"
                string += data["body"]
                messagebox.showinfo(f"Message de {data['_data']['notifyName']}", string)
            return "OK", 200

        @app.post("/message_revoke_everyone")
        def message_revoke_everyone():
            print(request.json)
            return "OK", 200

        @app.post("/disconnected")
        def disconnected():
            print(request.json)
            return "OK", 200

        @app.post("/media_uploaded")
        def media_uploaded():
            print(request.json)
            return "OK", 200

        @app.post("/message_reaction")
        def message_reaction():
            print(request.json)
            return "OK", 200

        self.flt = flt = Thread(target=lambda: app.run(port=3046, debug=False))
        flt.daemon = True
        flt.start()

        super().__init__()

    def import_players(self):
        used_passwords: list = []
        used_id: list = []
        with open("players.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            self.players = [SMSPlayer(player["name"], player["lastname"], player["phone"], used_passwords, used_id)
                            for player in data if player.get("play", True)]
        print("Joueurs importés")

    def send_info_all(self, message: str):
        print("Envoie de l'information")
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
            sendMessage(player.phone, new_message)

    def send_info(self, player: SMSPlayer, message: str):
        print(player.name, ":", message)
        sendMessage(player.phone, message)

    def send_role(self, player) -> None:
        """
        Envoie un sms au joueur indiquant son role et ses tâches
        :param player: SMSPlayer: Le joueur avec son numéro de téléphone
        """
        message = f"Bonjour {player.name} {player.lastname},\n"
        message += "Vous êtes un " + self.config["names"][player.role].upper()
        if player.role == "impostor" and len(self.impostors) > 1:
            impostors = " ".join([(joueur.name + " " + joueur.lastname) for joueur in self.impostors])
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
        if self.unpause_code in content:
            self.unpause_game()
            return True
        for task in player.tasks:
            print(task.type)
            if task.type == "validate_basic":
                print(task.keywords)
                for word in task.keywords:
                    if word in content:
                        self.task_done(player, task)
                        return True
            elif task.type == "activate_basic":
                print(task.activ_keywords)
                for word in task.activ_keywords:
                    if word in content:
                        sendMessage(player.phone, f"La tâche {task.name} vous envoie:\n{task.message}")
                        task.active = True
                        return True
            elif task.type == "activ_valid":
                print(task.keywords, task.activ_keywords)
                for word in task.keywords:
                    if word in content:
                        if task.active:
                            self.task_done(player, task)
                            sendMessage(player.phone, "Vous avez bien validé la tâche !")
                            return True
                        else:
                            sendMessage(player.phone, "La tâche n'est pas encore activée")
                            return True
                for word in task.activ_keywords:
                    if word in content:
                        sendMessage(player.phone, f"La tâche {task.name} vous envoie:\n{task.message}")
                        task.active = True
                        return True

        return False


if __name__ == '__main__':
    WhatsAppGame(True)
