#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import messagebox
from sms.airmore_manager import send_sms, get_new_messages
from classes import SMSPlayer
from game_class import Game
import json
from sms.commands import commands
import datetime
from threading import Timer


class SMSGame(Game):
    def __init__(self, game_master: bool = None):
        self.receive = True
        self.send_messages = []
        Timer(1, self.start_recieve_sms).start()

        super().__init__(game_master)

        print("Chargement des joueurs")

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
            send_sms(player.phone, new_message)

    def send_info(self, player: SMSPlayer, message: str):
        print(player.name, ":", message)
        send_sms(player.phone, message)

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
                        send_sms(player.phone, f"La tâche {task.name} vous envoie:\n{task.message}")
                        task.active = True
                        return True
            elif task.type == "activ_valid":
                for word in task.keywords:
                    if word in message:
                        if task.active:
                            self.task_done(player, task)
                            send_sms(player.phone, "Vous avez bien validé la tâche !")
                            return True
                        else:
                            send_sms(player.phone, "La tâche n'est pas encore activée")
                            return True
                for word in task.activ_keywords:
                    if word in message:
                        send_sms(player.phone, f"La tâche {task.name} vous envoie:\n{task.message}")
                        task.active = True
                        return True

        return False

    def start_recieve_sms(self):
        """
        Active la vérification périodique de la réception de SMS
        """

        def recieve():
            try:
                new = get_new_messages(self)
            except Exception as e:
                print(e)
                new = []
            if len(new) > 0:
                for msg in new:
                    if msg.content in self.send_messages:
                        del self.send_messages[self.send_messages.index(msg.content)]
                        continue
                    joueur = next((joueur for joueur in self.players if joueur.phone == msg.phone), None)
                    if self.check_command(joueur, msg.content):
                        continue
                    string = "Nouveau message de " + joueur.get_name() + " (" + joueur.phone + ") :\n"
                    string += msg.content
                    messagebox.showinfo(f"Message de {msg.phone}", string)

            for player in self.players:
                if player.last_message and player.last_message + self.config["min_before_inactiv_warn"] * 60 < int(
                        datetime.datetime.now().timestamp()):
                    print(player.get_name())
                    print(player.last_message, int(datetime.datetime.now().timestamp()))
                    print(player.last_message + self.config["min_before_inactiv_warn"] * 60 < int(datetime.datetime.now().timestamp()))
                    print(player.name, ":", "n'a pas donné de ses nouvelles depuis", self.config["min_before_inactiv_warn"] * 60, "secondes")

                    if player.last_warning and player.last_warning + self.config["min_before_inactiv_warn"] * 60 < int(
                            datetime.datetime.now().timestamp()):
                        print(player.name, ":", "n'a pas donné de ses nouvelles depuis", self.config["min_before_inactiv_warn"] * 60, "secondes")
                        if player.warnings >= self.config["max_warns"]:
                            print("Game pause")
                            # self.send_info_all(
                            #     f"{player.get_name()} n'a pas donné de ses nouvelles depuis {self.config['min_before_inactiv_warn'] * player.warnings} minutes. Le jeu est donc en pause le temps qu'on retrouve le joueur")
                            self.pause = True
                            if self.game_master:
                                messagebox.showerror("Un joueur ne répond pas",
                                                     f"{player.get_name()} n'a pas donné de ses nouvelles depuis {self.config['min_before_inactiv_warn'] * player.warnings} minutes. Le jeu est donc en pause le temps qu'on retrouve le joueur. Un message a été envoyé à tout le monde.")
                        else:
                            print("Warning")
                            # send_sms(player.phone,
                            #          f"Il y a un problème ? Nous n'avons pas reçu de message depuis {self.config['min_before_inactiv_warn'] * player.warnings} minutes. Si tout va bien, renvoie un message pour que nous soyons sûr que tout va bien.")
                            if self.game_master:
                                messagebox.showwarning("Sans nouvelles d'un joueur",
                                                       f"{player.get_name()} n'a plus envoyé de messages depuis {self.config['min_before_inactiv_warn'] * player.warnings} minutes. Un message d'avertissement lui a été envoyé. Une procédure d'urgence aura lieu automatiquement si on n'a pas de nouvelles dans {self.config['max_warns'] - player.warnings * self.config['min_before_inactiv_warn']} minutes")
                        player.warnings += 1
                        player.last_warning = int(datetime.datetime.now().timestamp())
                    elif not player.last_warning:
                        print("Warning")
                        player.warnings += 1
                        # send_sms(player.phone,
                        #          f"Il y a un problème ? Nous n'avons pas reçu de message depuis {self.config['min_before_inactiv_warn'] * player.warnings} minutes. Si tout va bien, renvoie un message pour que nous soyons sûr que tout va bien.")
                        if self.game_master:
                            messagebox.showwarning("Sans nouvelles d'un joueur",
                                                   f"{player.get_name()} n'a plus envoyé de messages depuis {self.config['min_before_inactiv_warn'] * player.warnings} minutes. Un message d'avertissement lui a été envoyé. Une procédure d'urgence aura lieu automatiquement si on n'a pas de nouvelles dans {self.config['max_warns'] - player.warnings * self.config['min_before_inactiv_warn']} minutes")
                        player.last_warning = int(datetime.datetime.now().timestamp())
                if self.receive:
                    Timer(5, recieve).start()

        Timer(2, recieve).start()


if __name__ == '__main__':
    SMSGame(True)
