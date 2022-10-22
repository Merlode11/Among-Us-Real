#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox, ttk
from smsManager import send_sms
from classes import SMSGame, SMSPlayer, Task
from utils import clear_frame


def start_game(game_master: bool = None):
    """
    Démare une partie en type SMS. Affiche la fenêtre du jeu
    """
    game = SMSGame()

    if game_master is None:
        game_master = game_master
    else:
        game.game_master = game_master

    window = Tk()
    window.title(game.config["names"]["title"])
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("amongus.ico")
    window.state("zoomed")

    # Check if the configuration is correct with the players
    if game.config["impostors"] + game.config["ingeniors"] + game.config["scientists"] > len(game.players):
        messagebox.showerror("Erreur", "Le nombre de joueurs est insuffisant pour la configuration choisie")
        return window.destroy()

    label_title = Label(window, text=game.config["names"]["title"], font=("Arial", 30))
    label_title.pack(fill=X)

    messagebox.showinfo("Bienvenue", "Bienvenue dans le jeu " + game.config["names"]["title"] + "\n"
                                                                                                "Une nouvelle partie va commencer.\n"
                                                                                                "Êtes-vous prêt à jouer ?")

    game.define_roles()
    game.define_tasks()

    def closing():
        """
        Affichage d'une fenêtre de confirmation de fermeture
        :return:
        """
        if messagebox.askokcancel("Quitter", "Êtes vous sûr de quitter ?"):
            game.send_messages.append("La partie s'est interommpue brutalement.")
            game.send_message_to_all("La partie s'est interommpue brutalement.")
            game.receive = False
            window.destroy()
            exit(-1)

    window.protocol("WM_DELETE_WINDOW", closing)

    def kill_player(player: SMSPlayer):
        """
        Tuer un joueur
        :param player: Player: Joueur à tuer
        :return:
        """
        player.dead = True
        game.dead_players.append(player)
        if player.role == "crewmate" or player.role == "ingenior" or player.role == "scientist":
            del game.crewmates[game.crewmates.index(player)]
        elif player.role == "impostor":
            del game.impostors[game.impostors.index(player)]

        if len(game.crewmates) <= len(game.impostors):
            game.send_message_to_all(
                "Tout les " + game.config["names"]["crewmate"].lower() + " sont morts, les " + game.config["names"][
                    "impostor"].lower() + " ont gagné !\nMerci de vous rendre immédiatement au point de rendez-vous !\n")
            show_players()
            response = messagebox.askyesno("Game Over",
                                           "Les " + game.config["names"]["impostor"].lower() + " ont gagné !\n"
                                                                                               "Tous les " +
                                           game.config["names"]["crewmate"].lower() + " ont été tués.\n"
                                                                                      "Voulez-vous recommencer ?")

            if response:
                window.destroy()
                start_game(game_master)
            else:
                window.destroy()
        elif len(game.impostors) == 0:
            show_players()
            response = messagebox.askyesno("Game Over",
                                           "Les " + game.config["names"]["crewmate"].lower() + " ont gagné !\n"
                                                                                               "Tous les " +
                                           game.config["names"]["impostor"].lower() + " ont été tués.\n"
                                                                                      "Voulez-vous recommencer ?")
            if response:
                window.destroy()
                start_game(game_master)
            else:
                window.destroy()
        else:
            send_sms(player.phone, "Vous avez été confirmé comme en tant que mort par le maître du jeu !")

    def reborn_player(player: SMSPlayer):
        """
        Réanimer un joueur
        :param player: Player: Joueur à réanimer
        :return:
        """
        player.dead = False
        del game.dead_players[game.dead_players.index(player)]
        if player.role == "impostor":
            game.impostors.append(player)
        else:
            game.crewmates.append(player)
        show_players()

    play_frame = Frame(window, width=800, height=600, bg="#f5f5f5")

    def show_players():
        """
        Afficher tous les joueurs dans le frame play_frame
        :return:
        """
        clear_frame(play_frame)
        for player in game.players:
            perso_frame = Frame(play_frame, width=800, height=100, bg="#f5f5f5", highlightbackground="#000000",
                                highlightthickness=1)
            bg = "#a9a9a9" if player.dead and game_master else "#f5f5f5"
            fg = "#000000"
            if player.role == "crewmate":
                fg = "#00b300"
            elif player.role == "impostor":
                fg = "#ff0000"
            elif player.role == "ingenior":
                fg = "#ffa500"
            elif player.role == "scientist":
                fg = "#0000ff"
            if not game_master:
                fg = "#000000"

            label_player = Label(perso_frame, text=player.get_str(game), font=("Arial", 20), bg=bg, fg=fg)
            label_player.pack(expand=True, side=LEFT)
            label_player.pack()

            send_message = Button(perso_frame, text="Envoyer un message",
                                  command=lambda joueur=player: send_message_window(joueur))
            send_message.pack(anchor="e", expand=YES, side=RIGHT)

            task_button = Button(perso_frame, text="Tâches", command=lambda joueur=player: show_tasks(joueur))
            if not game_master:
                task_button.configure(state="disabled")

            if player.finished_all_tasks() and game_master:
                task_button.config(bg="#00b300")

            task_button.pack(anchor="e", expand=YES, side=RIGHT)

            dead_button = Button(perso_frame, text="Mort", command=lambda joueur=player: kill_player(joueur))
            if player.dead:
                dead_button.configure(state="disabled")
            dead_button.pack(anchor="e", expand=YES, side=RIGHT)
            perso_frame.pack(fill=BOTH, expand=True)

            reborn_button = Button(perso_frame, text="Réapparaître",
                                   command=lambda joueur=player: reborn_player(joueur))
            if not player.dead:
                reborn_button.configure(state="disabled")
            reborn_button.pack(anchor="e", expand=YES, side=RIGHT)
            perso_frame.pack()

        cadavre_button = Button(play_frame, text="Cadavre", command=lambda: game.send_message_to_all(
            "Un cadavre a été signalé.\nMerci de vous rendre immédiatement au point de rendez vous !"))
        cadavre_button.pack(expand=YES, side=RIGHT)
        reunion_button = Button(play_frame, text="Réunion", command=lambda: game.send_message_to_all(
            "Une réunion a été demandée.\nMerci de vous rendre immédiatement au point de rendez vous !"))
        reunion_button.pack(expand=YES, side=LEFT)
        send_all_message_button = Button(play_frame, text="Envoyer un message",
                                         command=lambda: send_message_all_window())
        send_all_message_button.pack(expand=YES, side=LEFT)
        play_frame.pack()

    show_players()

    tasks_progress = Frame(window, width=800, height=100, bg="#f5f5f5")
    label_tasks = Label(tasks_progress, text=f"{len(game.done_tasks)}/{game.given_tasks} tâches données",
                        font=("Arial", 20))
    label_tasks.pack(fill=X, side=BOTTOM)
    tasks_progress_bar = ttk.Progressbar(tasks_progress, orient="horizontal", length=800, mode="determinate")
    tasks_progress_bar.pack(fill=X, side=BOTTOM)
    tasks_progress_bar.config(value=len(game.done_tasks) / game.given_tasks * 100)
    tasks_progress.pack(fill=X, side=BOTTOM)

    def show_tasks(player: SMSPlayer):
        """
        Affiche une fenêtre avec les tâches du joueur
        :param player: SMSPlayer: Joueur dont on veut afficher les tâches
        :return:
        """
        task_window = Tk()
        task_window.title(f"Tâches de {player.name} {player.lastname}")
        task_window.geometry("500x500")
        task_window.resizable(True, True)
        task_window.configure(background="white")
        task_window.iconbitmap("amongus.ico")
        task_window.focus_force()

        tasks_frame = Frame(task_window, bg="white")
        tasks_frame.pack(fill=BOTH, expand=True)

        def show_tasks_frame():
            """
            Affiche les tâches du joueur dans le frame tasks_frame
            """
            clear_frame(tasks_frame)
            for task in player.tasks:
                task_frame = Frame(tasks_frame, bg="white")
                if task.done:
                    bg = "#00b300"
                    fg = "#000000"
                else:
                    bg = "#f5f5f5"
                    fg = "#000000"
                task_label = Label(task_frame, text=task.__str__(), bg=bg, fg=fg, font="Arial 10")
                task_label.pack(expand=True, side=LEFT)
                task_done_button = Button(task_frame, text="Faite", command=lambda tache=task: task_done(tache))
                task_done_button.pack(anchor="e", expand=YES, side=RIGHT)
                task_undone_button = Button(task_frame, text="Non faite", command=lambda tache=task: task_undone(tache))
                task_undone_button.pack(anchor="e", expand=YES, side=RIGHT)
                if task.done:
                    task_done_button.configure(state="disabled")
                else:
                    task_undone_button.configure(state="disabled")
                if player.role == "impostor":
                    task_done_button.configure(state="disabled")
                    task_undone_button.configure(state="disabled")

                details_button = Button(task_frame, text="Détails", command=lambda tache=task: show_details(tache))
                details_button.pack(anchor="e", expand=YES, side=RIGHT)

                task_frame.pack(fill=BOTH, expand=True)

        show_tasks_frame()

        def task_done(task: Task):
            """
            Marque une tâche comme faite
            :param task: Task: Tâche à marquer comme faite
            """
            task.done = True
            game.done_tasks.append(task)
            tasks_progress_bar.config(value=len(game.done_tasks) / game.given_tasks * 100)
            label_tasks.config(text=f"{len(game.done_tasks)}/{game.given_tasks} tâches données")
            game.send_messages.append(f"Votre tâche {task.name} a été confirmée comme faite !")
            send_sms(player.phone, f"Votre tâche {task.name} a été confirmée comme faite !")

            if len(game.done_tasks) == game.given_tasks:
                task_window.destroy()
                tasks_progress_bar.config(value=100)
                game.send_message_to_all(
                    "Les mélenchonnistes ont gagné car ils ont terminé toutes leurs tâches !\nMerci de vous rendre "
                    "immédiatement au point de rendez vous !")
                response = messagebox.askyesno("Game Over", "Les mélenchonistes ont gagné !\n"
                                                            "Toutes les tâches ont été finies.\n"
                                                            "Voulez-vous recommencer ?")
                if response:
                    window.destroy()
                    start_game(game_master)
                else:
                    window.destroy()
            if player.finished_all_tasks():
                task_window.destroy()
                show_players()
                return True
            show_tasks_frame()

        def task_undone(task: Task):
            """
            Marque une tâche comme non faite
            :param task: Task: Tâche à marquer comme non faite
            :return:
            """
            task.done = False
            del game.done_tasks[game.done_tasks.index(task)]
            tasks_progress_bar.config(value=len(game.done_tasks) / game.given_tasks * 100)
            label_tasks.config(text=f"{len(game.done_tasks)}/{game.given_tasks} tâches données")
            show_tasks_frame()

        def show_details(task: Task):
            """
            Affiche les détails d'une tâche
            :param task:
            :return:
            """
            details = Tk()
            details.title(f"{task.name} ({task.classe})")
            details.geometry("500x250")
            details.resizable(True, True)
            details.iconbitmap("amongus.ico")
            details.configure(background="white")
            Label(details, text=task.description, bg="white", font="Arial 12",
                  wraplength=300, justify="center").pack()
            ttk.Separator(details, orient="horizontal").pack(fill="x")
            Label(details, text=task.location, bg="white", font="Arial 12",
                  wraplength=300, justify="center").pack()

            if task.other and task.other.get("questions"):
                ttk.Separator(details, orient="horizontal").pack(fill="x")
                Label(details, text="Questions", bg="white", font="Arial 12 bold",
                      wraplength=300, justify="center").pack()
                task.success = 0

                def valide_anwser():
                    """
                    Valide la réponse à la question
                    :return:
                    """
                    task.success += 1
                    if task.success >= len(task.other["questions"]) - 1:
                        task_done(task)
                        details.destroy()

                for i in range(len(task.other["questions"])):
                    ttk.Separator(details, orient="horizontal").pack(fill="x")
                    question = task.other["questions"][i]
                    Label(details, text=question["question"], bg="white", font="Arial 12",
                          wraplength=300, justify="center").pack()
                    Button(details, text="Valide", command=valide_anwser).pack()

                    answers_list = []
                    for answer in question["answers"]:
                        if answer["correct"]:
                            answers_list.append(f"[X] {answer['answer']}")
                        else:
                            answers_list.append(f"[ ] {answer['answer']}")
                    Label(details, text=" | ".join(answers_list), bg="white", font="Arial 12", ).pack()

            details.mainloop()

        task_window.mainloop()

    def send_message_all_window():
        """
        Affiche une fenêtre pour envoyer un message à tous les joueurs
        :return:
        """
        sender = Tk()
        sender.title("Envoyer un message")
        sender.geometry("500x100")
        sender.resizable(True, True)
        sender.configure(background="white")
        sender.iconbitmap("amongus.ico")
        sender.focus_force()

        message_frame = Frame(sender, bg="white")
        message_frame.pack(fill=BOTH, expand=True)

        message_entry = Entry(message_frame, width=100)
        message_entry.pack(fill=X, expand=YES, side=TOP)
        message_entry.focus_set()

        def send_message():
            message = message_entry.get()
            game.send_message_to_all(message)
            sender.destroy()

        sendButton = Button(message_frame, text="Envoyer", command=send_message)
        sendButton.pack(fill=X, expand=YES, side=BOTTOM)

        message_entry.bind("<Return>", send_message())

        sender.mainloop()

    def send_message_window(player: SMSPlayer):
        """
        Affiche la fenêtre d'envoi de message à un joueur spécifique
        """
        sender = Tk()
        sender.title("Envoyer un message")
        sender.geometry("500x100")
        sender.resizable(True, True)
        sender.configure(background="white")
        sender.iconbitmap("amongus.ico")
        sender.focus_force()

        messageFrame = Frame(sender, bg="white")
        messageFrame.pack(fill=BOTH, expand=True)

        messageEntry = Entry(messageFrame, width=100)
        messageEntry.pack(fill=X, expand=YES, side=TOP)
        messageEntry.focus_set()

        def send_message():
            """
            Envoyer le message entré
            """
            message = messageEntry.get()
            game.send_messages.append(message)
            send_sms(player.phone, message)
            sender.destroy()

        sendButton = Button(messageFrame, text="Envoyer", command=send_message)
        sendButton.pack(fill=X, expand=YES, side=BOTTOM)

        messageEntry.bind("<Return>", send_message())

        sender.mainloop()

    game.start_recieve_sms()
    window.mainloop()


if __name__ == '__main__':
    start_game()