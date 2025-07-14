#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from tkinter import messagebox

from android_sms_gateway import domain, client
from android_sms_gateway.enums import WebhookEvent
from android_sms_gateway.http import RequestsHttpClient
from flask import Flask, request

from classes import SMSPlayer
from game_class import Game
import json
from sms.commands import commands
import datetime
from threading import Timer, Thread
import socket


class SMSGame(Game):
    def __init__(self, game_master: bool = None):
        self.receive = True
        self.send_messages = []
        self.server = app = Flask(__name__)

        @app.post("/message")
        def message():
            data = request.json.get("data", {}).get("payload", {})
            joueur = next((player for player in self.players if
                           player.phone == data["phoneNumber"]), None)
            if self.import_window is not None:
                if self.register_code in data["message"]:
                    if joueur is not None:
                        return self.send_info(joueur, "Vous êtes déjà enregistré dans la partie !")
                    new_player = {
                        "type": "sms",
                        "name": data["message"].replace(self.register_code, ""),
                        "phone": f"{data['phoneNumber']}",
                        "play": True,
                    }
                    player = SMSPlayer(new_player["name"], new_player["phone"], self.used_passwords, self.used_id)
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
                    return True
            if not self.check_command(joueur, data):
                string = "Nouveau message de " + joueur.get_name() + " (" + joueur.phone + ") :\n"
                string += data["message"]
                messagebox.showinfo(f"Message de {joueur.get_name()}", string)
            return "OK", 200

        self.flt = flt = Thread(target=lambda: app.run(port=3046, debug=False))
        flt.daemon = True
        flt.start()

        with open(os.path.dirname(os.path.abspath(__file__)).replace("\\sms", "") + "\\config.json", "r", encoding='utf-8') as f:
            self.config = json.load(f)

        with RequestsHttpClient() as h, client.APIClient(
            self.config["sms_username"],
            self.config["sms_password"],
            base_url=f"http://{self.config['ip']}:{self.config['port']}" + (
                "/3rdparty/v1" if "api.sms-gate.app" in self.config['ip'] else ""),
            http=h,
        ) as c:
            self.client = c
            # Get the actual local IP
            ip = socket.gethostbyname(socket.gethostname())
            self.webhook = c.create_webhook(
                domain.Webhook("Webhook1", f"http://{ip}:3046/message",
                               WebhookEvent.SMS_RECEIVED))

        print("Chargement des joueurs")

        super().__init__(game_master)

    def import_players(self):
        used_passwords: list = []
        used_id: list = []
        with open("players.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            self.players = [SMSPlayer(player["name"], player["phone"], used_passwords, used_id)
                            for player in data if player.get("play", True)]
        print("Joueurs importés")

        messagebox.showinfo("Bienvenue", "Bienvenue dans le jeu " + self.config["names"]["title"] + "\n" +
                            "Une nouvelle partie va commencer.\n" +
                            "Êtes-vous prêt à jouer ?")

        self.start_game()

    def send_info_all(self, message: str):
        print("Envoie de l'information")
        for player in self.players:
            new_message = message.replace("{name}", player.name)
            # replace the variable in the message
            new_message = new_message.replace("{role}", self.config["names"][player.role])
            new_message = new_message.replace("{id}", player.id)
            new_message = new_message.replace("{phone}", player.phone)
            new_message = new_message.replace("{tasks}", "\n".join([task.name for task in player.tasks]))
            new_message = new_message.replace("{password}", player.password)

            print(player.name, ":", new_message)
            self.send_info(player, new_message)

    def send_info(self, player: SMSPlayer, message: str):
        print(player.name, ":", message)
        sms = domain.Message(
            message,
            [player.phone],
        )
        self.client.send(sms)

    def send_role(self, player) -> None:
        """
        Envoie un sms au joueur indiquant son role et ses tâches
        :param player: SMSPlayer: Le joueur avec son numéro de téléphone
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
        if self.unpause_code in message and self.pause:
            self.unpause_game()
            return True
        for task in player.tasks:
            if task.type == "validate_basic":
                print(task.keywords)
                for word in task.keywords:
                    if word in message:
                        self.task_done(player, task)
                        return True
            elif task.type == "activate_basic":
                for word in task.activ_keywords:
                    if word in message:
                        self.send_info(player.phone, f"La tâche {task.name} vous envoie:\n{task.message}")
                        task.active = True
                        return True
            elif task.type == "activ_valid":
                for word in task.keywords:
                    if word in message:
                        if task.active:
                            self.task_done(player, task)
                            self.send_info(player.phone, "Vous avez bien validé la tâche !")
                            return True
                        else:
                            self.send_info(player.phone, "La tâche n'est pas encore activée")
                            return True
                for word in task.activ_keywords:
                    if word in message:
                        self.send_info(player.phone, f"La tâche {task.name} vous envoie:\n{task.message}")
                        task.active = True
                        return True

        return False

    def end_game(self):
        """
        Termine la partie
        :return:
        """
        self.receive = False
        self.client.delete_webhook(self.webhook.id)
        self.window.destroy()


if __name__ == '__main__':
    SMSGame(True)
