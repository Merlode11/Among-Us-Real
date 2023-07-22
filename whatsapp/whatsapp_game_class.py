#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import messagebox, ttk
from classes import SMSPlayer, BasicTask, show_phone_number
from game_class import Game
import json
import random
from whatsapp.commands import commands
from whatsapp.whatsapp_manager import send_message, get_user
from flask import Flask, request
from threading import Thread
import os


class WhatsAppGame(Game):
    def __init__(self, game_master: bool = None):
        self.receive = True
        self.send_messages = []
        self.server = app = Flask(__name__)
        # Start the NodeJs process to manage the whatsapp connection and get the logs from the process in a thread
        # Detect if there is a node_modules folder
        if not os.path.isdir("whatsapp/api/node_modules"):
            print("Installation des dépendances de WhatsApp")
            os.system("cd whatsapp/api && npm install")
        self.whatsapp_manager = Thread(target=lambda: os.system("cd whatsapp/api && node index.js"))
        self.whatsapp_manager.start()

        self.is_ready = False

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
            if not self.pause: 
                if self.import_window is not None:
                    self.is_ready = True
                else: 
                    messagebox.showinfo("Bienvenue", "Bienvenue dans le jeu " + self.config["names"]["title"] + "\n" +
                                        "Une nouvelle partie va commencer.\n" +
                                        "Êtes-vous prêt à jouer ?")
                    self.start_game()
            else:
                self.unpause_game()
            return "OK", 200

        @app.post("/message")
        def message():
            data = request.json["data"]
            if len(data["from"]) > 16:
                return "OK", 200
            joueur = next((player for player in self.players if
                           player.phone.replace("+", "") == data["from"].replace("@c.us", "")), None)
            if self.import_window is not None:
                if self.register_code in data["body"]:
                    if joueur is not None:
                        return self.send_info(joueur, "Vous êtes déjà enregistré dans la partie !")
                    new_player = {
                        "type": "sms"
                        "name": data['_data']['notifyName'], 
                        "phone": f"+{data["from"].replace("@c.us", ""))}"
                    }
                    self.players.append(SMSPlayer(new_player["name"], new_player["phone"], self.used_passwords, self.used_id))
                    if self.config["save_register"]:
                        
                        players = []
                        if os.path.exists("players.json"):
                            with open("players.json", "r", encoding="utf-8") as file:
                                players = json.load(file)
                        players.append(new_player)
                        with open("players.json", "w", encoding="utf-8") as file:
                            json.dump(players, file, indent=4, ensure_ascii=False)
                    self.send_info()
                    self.import_players()
                    return True
            if len(data["from"]) > 16:
                return "OK", 200
            joueur = next((player for player in self.players if
                           player.phone.replace("+", "") == data["from"].replace("@c.us", "")), None)
            if not self.check_command(joueur, data):
                string = "Nouveau message de " + joueur.get_name() + " (" + joueur.phone + ") :\n"
                string += data["body"]
                messagebox.showinfo(f"Message de {data['_data']['notifyName']}", string)
            return "OK", 200

        @app.post("/disconnected")
        def disconnected():
            self.pause = True
            self.pause_reason = "WhatsApp s'est déconnecté"
            self.set_pause_code()
            messagebox.showerror("Erreur", "WhatsApp s'est déconnecté.\nMerci de bien vouloir vérifier votre connexion.")
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
        if self.config["register_type"] == "liste": 
            with open("players.json", "r", encoding='utf-8') as f:
                data = json.load(f)
                self.players = [SMSPlayer(player["name"], player["phone"], used_passwords, used_id)
                                for player in data if player.get("play", True) and player.get("type", "") == "sms"]
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
            
            whatsapp_user = get_user()
    
            url_label = Label(qrcode_frame, text=f"Envoyez {self.register_code} à {show_phone_number(whatsapp_user["wid"])} pour vous enregistrer", font=("Arial", 28))
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
            new_message = new_message.replace("{phone}", player.phone)
            new_message = new_message.replace("{tasks}", "\n".join([task.name for task in player.tasks]))
            new_message = new_message.replace("{password}", player.password)

            print(player.name, ":", new_message)
            send_message(player.phone, new_message)

    def send_info(self, player: SMSPlayer, message: str):
        print(player.name, ":", message)
        send_message(player.phone, message)

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
                        send_message(player.phone, f"La tâche {task.name} vous envoie:\n{task.message}")
                        task.active = True
                        return True
            elif task.type == "activ_valid":
                for word in task.keywords:
                    if word in content:
                        if task.active:
                            self.task_done(player, task)
                            send_message(player.phone, "Vous avez bien validé la tâche !")
                            return True
                        else:
                            send_message(player.phone, "La tâche n'est pas encore activée")
                            return True
                for word in task.activ_keywords:
                    if word in content:
                        send_message(player.phone, f"La tâche {task.name} vous envoie:\n{task.message}")
                        task.active = True
                        return True

        return False


if __name__ == '__main__':
    WhatsAppGame(True)
