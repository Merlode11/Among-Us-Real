#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox, ttk

from classes import Player, SMSPlayer, set_task
from utils import clear_frame, VerticalScrolledFrame, Timer
import json
import random
import os
from playsound import playsound


class Game:
    def __init__(self, game_master: bool = None):
        self.path = os.path.dirname(os.path.abspath(__file__))

        with open(self.path + "/config.json", "r", encoding='utf-8') as f:
            self.config = json.load(f)

        self.given_tasks: int = 0

        self.crewmates: list = []
        self.impostors: list = []
        self.dead_players: list = []
        self.done_tasks: list = []
        self.meeting: str or None = None
        self.meeting_votes: dict = {}
        self.meeting_here_users: list = []
        self.end: bool = False

        if game_master is None:
            self.game_master: bool = self.config["game_master"]
        else:
            self.game_master: bool = game_master

        self.pause: bool = False
        self.unpause_code: str = ""
        self.pause_reason: str = ""
        self.pause_pop = None

        # Game window
        self.window = window = Tk()
        window.title(self.config["names"]["title"])
        window.geometry("800x600")
        window.resizable(True, True)
        window.iconbitmap(self.path + "/assets/img/amongus.ico")
        window.state("zoomed")

        # Check if the task list exists
        if not os.path.exists(self.path + r"/taskList/" + self.config["task_list"] + ".json"):
            messagebox.showerror("Erreur", "La liste de tâches sélectionnée n'existe pas !")
            self.window.destroy()
            return
        self.tasks: list = []
        with open(self.path + r"/taskList/" + self.config["task_list"] + ".json", "r", encoding='utf-8') as f:
            data = json.load(f)
            self.tasks = [set_task(task) for task in data]
        if len(self.tasks) < self.config["tasks"]:
            messagebox.showerror("Erreur", "Le nombre de tâches à donner est supérieur au nombre de tâches "
                                           "disponibles !")
            self.window.destroy()
            return

        self.players: list = []
        self.import_players()

        self.__label_title = None
        self.__buttons_frame = None
        self.__tasks_progress = None
        self.__label_tasks = None
        self.__tasks_progress_bar = None
        self.__play_frame = None

        window.mainloop()

    def start_game(self):
        """
        Démarre la partie
        :return:
        """
        window = self.window

        if len(self.tasks) < self.config["tasks"]:
            messagebox.showerror("Erreur",
                                 "Le nombre de tâches à donner est supérieur au nombre de tâches disponibles !",
                                 parent=window)
            self.window.destroy()
            return

        if self.config["impostors"] + self.config["engineers"] + self.config["scientists"] > len(self.players):
            messagebox.showerror("Erreur", "Le nombre de joueurs est insuffisant pour la configuration choisie")
            self.window.destroy()
            return

        self.__label_title = label_title = Label(self.window, text=self.config["names"]["title"], font=("Arial", 30))
        label_title.pack(fill=X)

        for joueur in self.players:
            print(joueur.get_name(), joueur.role, joueur.id, joueur.password)

        self.define_roles()
        self.define_tasks()

        def closing():
            """
            Fonction de fermeture de la fenêtre
            """
            if messagebox.askokcancel("Quitter", "Êtes vous sûr de quitter ?"):
                self.send_info_all("La partie s'est interommpue brutalement.")
                self.end_game()

        window.protocol("WM_DELETE_WINDOW", closing)

        self.__buttons_frame = global_buttons_frame = Frame(self.window, bg="#f5f5f5")
        cadavre_button = Button(global_buttons_frame, text="Cadavre", font=("Arial", 15),
                                command=lambda: self.start_meeting(
                                    "Un cadavre a été signalé."))
        cadavre_button.pack(expand=YES, side=LEFT)
        reunion_button = Button(global_buttons_frame, text="Réunion", font=("Arial", 25),
                                command=lambda: self.start_meeting(
                                    "Une réunion a été demandée."))
        reunion_button.pack(expand=YES, side=LEFT)
        send_all_message_button = Button(global_buttons_frame, text="Envoyer un message à tous", font=("Arial", 15),
                                         command=lambda: self.send_message_all_window())
        send_all_message_button.pack(expand=YES, side=LEFT)
        global_buttons_frame.pack(fill=X, expand=YES, side=TOP)

        if not self.game_master:
            cadavre_button.pack_forget()
            send_all_message_button.pack_forget()

        self.__tasks_progress = tasks_progress = Frame(window, width=800, height=100, bg="#f5f5f5")
        self.__label_tasks = label_tasks = Label(tasks_progress,
                                                 text=f"{len(self.done_tasks)}/{self.given_tasks} tâches données",
                                                 font=("Arial", 20))
        label_tasks.pack(fill=X, side=BOTTOM)
        self.__tasks_progress_bar = tasks_progress_bar = ttk.Progressbar(tasks_progress, orient="horizontal",
                                                                         length=800, mode="determinate")
        tasks_progress_bar.pack(fill=X, side=BOTTOM)
        tasks_progress_bar.config(value=len(self.done_tasks) / self.given_tasks * 100)
        tasks_progress.pack(fill=X, side=BOTTOM)

        self.__play_frame = play_frame = VerticalScrolledFrame(window, width=800, height=600, bg="#f5f5f5")
        self.show_players()

        play_frame.pack(fill=BOTH, expand=YES)

        window.mainloop()

    def show_players(self):
        """
        Afficher tous les joueurs dans le frame play_frame
        :return:
        """
        play_frame = self.__play_frame
        clear_frame(play_frame)
        for player in self.players:
            perso_frame = Frame(play_frame, width=800, height=100, bg="#f5f5f5", highlightbackground="#000000",
                                highlightthickness=1)
            bg = "#a9a9a9" if player.dead and self.game_master else "#f5f5f5"
            fg = "#000000"
            if player.role == "crewmate":
                fg = "#00b300"
            elif player.role == "impostor":
                fg = "#ff0000"
            elif player.role == "engineer":
                fg = "#ffa500"
            elif player.role == "scientist":
                fg = "#0000ff"
            if not self.game_master:
                fg = "#000000"

            label_frame = Frame(perso_frame, width=800, height=100, bg=bg)
            label_player = Label(label_frame, text=player.get_str(self), font=("Arial", 20), bg=bg, fg=fg)
            label_player.grid(row=0, column=0, sticky=W)
            label_frame.pack(fill=X, anchor=W, side=LEFT)

            buttons_frame = Frame(perso_frame, width=800, height=100, bg=bg)

            def toogle_button(joueur: SMSPlayer):
                if joueur.dead:
                    self.reborn_player(joueur)
                    dead_button.config(text="Mort")
                else:
                    self.kill_player(joueur)
                    dead_button.config(text="Mettre Vivant")

            dead_button = Button(buttons_frame, text="Mort", command=lambda joueur=player: toogle_button(joueur))
            if not self.game_master:
                dead_button.configure(state="disabled")
            dead_button.grid(row=0, column=1, sticky=E)

            task_button = Button(buttons_frame, text="Tâches", command=lambda joueur=player: show_tasks(joueur))
            if not self.game_master:
                task_button.configure(state="disabled")

            if player.finished_all_tasks() and self.game_master:
                task_button.config(bg="#00b300")

            task_button.grid(row=0, column=2, sticky=E)

            send_message = Button(buttons_frame, text="Envoyer un message",
                                  command=lambda joueur=player: self.send_message_window(joueur))
            send_message.grid(row=0, column=3, sticky=E)

            buttons_frame.pack(fill=X, anchor=E, side=RIGHT)
            if not self.game_master:
                buttons_frame.pack_forget()

            perso_frame.pack(fill=BOTH, expand=True)

        play_frame.pack()

        def show_tasks(joueur: Player):
            """
            Affiche une fenêtre avec les tâches du joueur
            :param joueur: Player: Joueur dont on veut afficher les tâches
            :return:
            """
            task_window = Tk()
            task_window.title(f"Tâches de {joueur.get_str(self)}")
            task_window.geometry("500x500")
            task_window.resizable(True, True)
            task_window.configure(background="white")
            task_window.iconbitmap(self.path + "/assets/img/amongus.ico")
            task_window.focus_force()

            tasks_frame = Frame(task_window, bg="white")
            tasks_frame.pack(fill=BOTH, expand=True)

            def show_tasks_frame():
                """
                Affiche les tâches du joueur dans le frame tasks_frame
                """
                clear_frame(tasks_frame)
                for task in joueur.tasks:
                    task_frame = Frame(tasks_frame, bg="white")
                    if task.done:
                        background = "#00b300"
                        foreground = "#000000"
                    else:
                        background = "#f5f5f5"
                        foreground = "#000000"
                    task_label = Label(task_frame, text=str(task), bg=background, fg=foreground, font="Arial 10")
                    task_label.pack(expand=True, side=LEFT)
                    task_done_button = Button(task_frame, text="Faite", command=lambda tache=task: task_done(tache))
                    task_done_button.pack(anchor="e", expand=YES, side=RIGHT)
                    task_undone_button = Button(task_frame, text="Non faite",
                                                command=lambda tache=task: task_undone(tache))
                    task_undone_button.pack(anchor="e", expand=YES, side=RIGHT)
                    if task.done:
                        task_done_button.configure(state="disabled")
                    else:
                        task_undone_button.configure(state="disabled")
                    if joueur.role == "impostor":
                        task_done_button.configure(state="disabled")
                        task_undone_button.configure(state="disabled")

                    details_button = Button(task_frame, text="Détails", command=lambda tache=task: show_details(tache))
                    details_button.pack(anchor="e", expand=YES, side=RIGHT)

                    task_frame.pack(fill=BOTH, expand=True)

            show_tasks_frame()

            def task_done(task):
                """
                Marque une tâche comme faite
                :param task: BasicTask: Tâche à marquer comme faite
                """
                if len(self.done_tasks) == self.given_tasks:
                    task_window.destroy()

                self.task_done(joueur, task)

                if joueur.finished_all_tasks():
                    task_window.destroy()
                    self.show_players()
                    return True
                show_tasks_frame()

            def task_undone(task):
                """
                Marque une tâche comme non faite
                :param task: BasicTask: Tâche à marquer comme non faite
                :return:
                """
                task.done = False
                del self.done_tasks[self.done_tasks.index(task)]
                self.__tasks_progress_bar.config(value=len(self.done_tasks) / self.given_tasks * 100)
                self.__label_tasks.config(text=f"{len(self.done_tasks)}/{self.given_tasks} tâches données")
                show_tasks_frame()

            def show_details(task):
                """
                Affiche les détails d'une tâche
                :param task:
                :return:
                """
                details = Tk()
                details.title(f"{str(task)} - Détails")
                details.geometry("500x250")
                details.resizable(True, True)
                details.iconbitmap(self.path + "/assets/img/amongus.ico")
                details.configure(background="white")
                Label(details, text=task.description, bg="white", font="Arial 12",
                      wraplength=300, justify="center").pack()
                ttk.Separator(details, orient="horizontal").pack(fill="x")
                Label(details, text=task.location, bg="white", font="Arial 12",
                      wraplength=300, justify="center").pack()

                details.mainloop()

            task_window.mainloop()

    def send_message_all_window(self):
        """
        Affiche une fenêtre pour envoyer un message à tous les joueurs
        :return:
        """
        sender = Tk()
        sender.title("Envoyer un message")
        sender.geometry("500x100")
        sender.resizable(True, True)
        sender.configure(background="white")
        sender.iconbitmap(self.path + "/assets/img/amongus.ico")
        sender.focus_force()

        message_frame = Frame(sender, bg="white")
        message_frame.pack(fill=BOTH, expand=True)

        message_entry = Entry(message_frame, width=100)
        message_entry.pack(fill=X, expand=YES, side=TOP)
        message_entry.focus_set()

        def send_message_to_all():
            message = message_entry.get()
            self.send_info_all(message)
            sender.destroy()

        sendButton = Button(message_frame, text="Envoyer", command=send_message_to_all)
        sendButton.pack(fill=X, expand=YES, side=BOTTOM)

        message_entry.bind("<Return>", send_message_to_all)

        sender.mainloop()

    def kill_player(self, player: Player):
        """
        Tuer un joueur
        :param player: Player: Joueur à tuer
        :return:
        """
        player.dead = True
        self.dead_players.append(player)
        if player.role == "crewmate" or player.role == "engineer" or player.role == "scientist":
            del self.crewmates[self.crewmates.index(player)]
        elif player.role == "impostor":
            del self.impostors[self.impostors.index(player)]

        if len(self.crewmates) <= len(self.impostors):
            self.send_info_all(
                "Tous les " + self.config["names"]["crewmate"].lower() + " sont morts, les " + self.config["names"][
                    "impostor"].lower() + "s ont gagné !\nMerci de vous rendre immédiatement au point de rendez-vous "
                                          "!\n")
            self.end = True
            self.show_players()
            response = messagebox.askyesno("Game Over",
                                           "Les " + self.config["names"]["impostor"].lower() + " ont gagné !\n"
                                                                                               "Tous les " +
                                           self.config["names"]["crewmate"].lower() + " ont été tués.\n"
                                                                                      "Voulez-vous recommencer ?",
                                           parent=self.window)

            self.end_game()
        elif len(self.impostors) == 0:
            self.show_players()
            self.end = True
            self.send_info_all(
                "Tous les " + self.config["names"]["impostor"].lower() + "s sont morts, les " + self.config["names"][
                    "crewmate"].lower() + "s ont gagné !\nMerci de vous rendre immédiatement au point de rendez-vous "
                                          "!\n")
            messagebox.askyesno("Game Over",
                                "Les " + self.config["names"]["crewmate"].lower() + " ont gagné !\n"
                                                                                    "Tous les " +
                                self.config["names"]["impostor"].lower() + "s ont été tués.\n"
                                                                           "Voulez-vous recommencer ?",
                                parent=self.window)
            self.end_game()
        else:
            self.show_players()
            self.send_info(player, "Vous avez été confirmé comme en tant que mort !")

    def end_game(self):
        """
        Termine la partie
        :return:
        """
        self.window.destroy()

    def reborn_player(self, player: Player):
        """
        Faire revenir un joueur à la vie
        :param player: Player: Joueur à faire revenir à la vie
        :return:
        """
        player.dead = False
        self.dead_players.remove(player)
        if player.role == "crewmate" or player.role == "engineer" or player.role == "scientist":
            self.crewmates.append(player)
        elif player.role == "impostor":
            self.impostors.append(player)
        self.show_players()
        self.send_info(player, "Vous avez été confirmé comme en tant que vivant par le maître du jeu !")

    def define_roles(self) -> None:
        """
        Défini les rôles de chacun des participants
        """
        random.shuffle(self.players)
        for i in range(self.config["impostors"]):
            self.impostors.append(self.players[i])
            self.players[i].role = "impostor"
        self.crewmates = self.players[self.config["impostors"]:]

        for player in self.crewmates:
            player.role = "crewmate"
        for player in self.impostors:
            player.role = "impostor"

        for i in range(self.config["engineers"]):
            self.crewmates[i].role = "engineer"
        for i in range(self.config["scientists"]):
            self.crewmates[i + self.config["engineers"]].role = "scientist"

        self.players = sorted(self.players, key=lambda joueur: joueur.get_name())

    def define_tasks(self) -> None:
        """
        Défini les tâches du joueur pour chaque participant
        """
        for player in self.players:
            random.shuffle(self.tasks)
            for i in range(self.config["tasks"]):
                player.tasks.append(set_task(self.tasks[i].to_dict()))
                self.tasks[i].nb_given += 1
                if self.tasks[i].nb_given >= self.config["max_task_given"]:
                    del self.tasks[i]
            if player.role != "impostor":
                self.given_tasks += self.config["tasks"]
            self.send_role(player)

    def send_role(self, player):
        pass

    def send_message_window(self, player: Player):
        """
        Affiche la fenêtre d'envoi de message à un joueur spécifique
        """
        sender = Tk()
        sender.title("Envoyer un message")
        sender.geometry("500x100")
        sender.resizable(True, True)
        sender.configure(background="white")
        sender.iconbitmap(self.path + "/assets/img/amongus.ico")
        sender.focus_force()

        messageFrame = Frame(sender, bg="white")
        messageFrame.pack(fill=BOTH, expand=True)

        messageEntry = Entry(messageFrame, width=100)
        messageEntry.pack(fill=X, expand=YES, side=TOP)
        messageEntry.focus_set()

        def send_message_player():
            """
            Envoyer le message entré
            """
            message = messageEntry.get()
            self.send_info(player, message)
            sender.destroy()

        sendButton = Button(messageFrame, text="Envoyer", command=send_message_player)
        sendButton.pack(fill=X, expand=YES, side=BOTTOM)

        messageEntry.bind("<Return>", lambda _: send_message_player())

        sender.mainloop()

    def set_pause_game(self):
        """
        Définir le code d'arrêt de la partie
        """
        code_int = random.randint(0, 1000)
        self.unpause_code = code_str = f"{code_int}"
        if self.game_master:
            self.pause_pop = pop = Toplevel(self.window)
            pop.title("Button de reprise")
            pop.geometry("300x100")
            pop.resizable(False, False)
            pop.iconbitmap(self.path + "/assets/img/amongus.ico")
            Label(pop, text="Code de reprise: " + code_str, font=("Arial", 20)).pack()

            Button(pop, text="Rétablir la partie", command=self.unpause_game).pack()
            self.pause = True

        return code_str

    def unpause_game(self):
        """
        Rétablit la partie
        :return:
        """
        self.pause = False
        self.pause_reason = ""
        self.unpause_code = ""
        self.pause_pop.destroy()
        self.send_info_all("La partie a été rétablie !")

    def start_meeting(self, message: str):
        """
        Démarre une réunion
        :param message: str: Raison de la réunion
        :return:
        """
        self.meeting = "coming"
        self.send_info_all(
            message + "\nMerci de vous rendre immédiatement au point de rendez-vous !\nRappel de votre code de "
                      "présence: {password}")
        window = Tk()
        window.title("Réunion")
        window.geometry("500x500")
        window.resizable(False, False)
        window.state("zoomed")
        window.iconbitmap(self.path + "/assets/img/amongus.ico")

        Label(window, text="Réunion", font=("Arial", 30)).pack()
        Label(window, text="Veuillez choisir un joueur à éliminer", font=("Arial", 20)).pack()
        Label(window, text="ou appuyer sur le bouton pour passer", font=("Arial", 20)).pack()
        Label(window, text="à la prochaine étape", font=("Arial", 20)).pack()

        players_here_frame = VerticalScrolledFrame(window)
        self.meeting_here_users = here_users = []

        def show_players():
            clear_frame(players_here_frame)
            for player in self.players:
                print(player.get_name(), ":", player.password)
                if player in here_users:
                    color = "green"
                else:
                    color = "red"
                if player.dead:
                    Label(players_here_frame, text=player.get_name(), font=("Arial", 20, "italic"),
                          fg=color).pack()
                else:
                    Label(players_here_frame, text=player.get_name(), font=("Arial", 20),
                          fg=color).pack()

        def present(password: str):
            if password not in [player.password for player in self.players]:
                messagebox.showerror("Erreur", "Code de présence invalide", parent=window)
            for player in self.players:
                if player.password == password:
                    if player in here_users:
                        messagebox.showerror("Erreur", "Vous êtes déjà présent", parent=window)
                    else:
                        # temporary for testing TODO: remove
                        # here_users.extend(self.players)
                        here_users.append(player)
                    show_players()
                    present_entry.delete(0, END)

                    if len(here_users) == len(self.players):
                        window.destroy()
                        self.meeting = "discussion"
                        self.timer = Timer(self.config.get("discussion_time", 0), "Discussion", self)

                        self.meeting = "vote"
                        vote_string = "C'est le moment de voter ! Votez pour le joueur à éliminer:"
                        vote_string += "\n0 - Passer à la prochaine étape (skip)"
                        for i in range(len(self.players)):
                            player = self.players[i]
                            if not player.dead:
                                vote_string += f"\n{i + 1} - {player.get_name()}"
                        vote_string += f"\n\nVotez avec la commande 'vote NUMERO'"
                        self.send_info_all(vote_string)
                        self.timer = Timer(self.config.get("vote_time", 0), "Vote", self)

                        # found killed player
                        votes = {}
                        for choice in self.meeting_votes.values():
                            if choice not in votes:
                                votes[choice] = 1
                            else:
                                votes[choice] += 1

                        highest_vote = 0
                        for player_id, vote_number in votes.items():
                            if vote_number > highest_vote:
                                highest_vote = vote_number
                        voted_player_id = "0"
                        if [vote_number for vote_number in votes.values()].count(highest_vote) == 1:
                            for player_id, vote_number in votes.items():
                                if vote_number == highest_vote:
                                    voted_player_id = player_id

                        killed_window = Tk()
                        killed_window.title("Élimination")
                        killed_window.geometry("500x500")
                        killed_window.resizable(False, False)
                        killed_window.state("zoomed")
                        killed_window.iconbitmap(self.path + "/assets/img/amongus.ico")

                        killed_text = "Personne (skip)"
                        if voted_player_id != "0":
                            player = self.get_player(voted_player_id)
                            killed_window.after(5000, lambda: self.kill_player(player))
                            killed_text = player.get_name()
                            if self.config["show_dead_roles"]: 
                                killed_text += f" ({self.config["names"][player.role]})"
                        
                        killed_text += " a été éliminé"

                        Label(killed_window, text="Élimination", font=("Arial", 30)).pack(fill=BOTH, expand=True,
                                                                                          padx=10)

                        Label(killed_window, text=killed_text,
                              font=("Arial", 20)).pack(fill=BOTH, expand=True, padx=10)

                        self.meeting_here_users = []
                        self.meeting = None
                        self.meeting_votes = {}

                        killed_window.after(10000, killed_window.destroy)
                        playsound(r"assets/sounds/eject.mp3", block=False)
                        killed_window.mainloop()
                    return

        Label(window, text="", ).pack()
        present_label = Label(window, text="Indiquer que vous êtes présent :", font=("Arial", 20))
        present_entry = Entry(window, font=("Arial", 20))
        present_button = Button(window, text="Valider", font=("Arial", 20),
                                command=lambda: present(present_entry.get()))
        present_label.pack()
        present_entry.pack()
        present_button.pack()

        present_entry.bind("<Return>", lambda event: present(present_entry.get()))

        show_players()

        Label(window, text="").pack()

        players_here_frame.pack()

        window.mainloop()

    def get_player(self, player_id: str) -> Player or None:
        """
        Récupérer un joueur à partir de son ID
        :param player_id: str: ID du joueur
        :return: Player: Joueur
        """
        for player in self.players:
            if player is not None and player.id == player_id:
                return player
        else:
            return None

    def import_players(self):
        pass

    def send_info_all(self, message: str):
        print("Envoie de l'information")
        for player in self.players:
            print(player.name, ":", message)

    def send_info(self, player: Player, message: str):
        pass

    def task_done(self, player: Player, task):
        task.done = True
        self.done_tasks.append(task)
        self.__tasks_progress_bar.config(value=len(self.done_tasks) / self.given_tasks * 100)
        self.__label_tasks.config(text=f"{len(self.done_tasks)}/{self.given_tasks} tâches données")
        self.show_players()

        if len(self.done_tasks) == self.given_tasks:
            self.__tasks_progress_bar.config(value=100)
            self.end = True
            self.send_info_all(
                "Les " + self.config["names"][
                    "crewmate"] + " ont gagné car ils ont terminé toutes leurs tâches !\nMerci de vous rendre "
                                  "immédiatement au point de rendez vous !")
            messagebox.askyesno("Game Over", "Les " + self.config["names"]["crewmate"] + " ont gagné !\n"
                                                                                         "Toutes les tâches ont été "
                                                                                         "finies.\n"
                                                                                         "Voulez-vous recommencer ?")
            self.end_game()
        elif self.game_master:
            messagebox.showinfo("Succès", f"{str(player)} a confirmé avoir réalisé la tâche {task.name} !")


if __name__ == '__main__':
    Game(True)
