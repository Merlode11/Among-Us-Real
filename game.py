#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
from tkinter import *
from tkinter import messagebox, ttk
from smsManager import send_sms, get_new_messages
from classes import Game, Player, Task


def start_game(game_master: bool = None):
    game = Game()
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

    label_title = Label(window, text=game.config["names"]["title"], font=("Arial", 30))
    label_title.pack(fill=X)

    messagebox.showinfo("Bienvenue", "Bienvenue dans le jeu " + game.config["names"]["title"] + "\n"
                                     "Une nouvelle partie va commencer.\n"
                                     "Êtes-vous prêt à jouer ?")

    game.define_roles()
    game.define_tasks()

    def closing():
        if messagebox.askokcancel("Quitter", "Êtes vous sûr de quitter ?"):
            game.send_messages.append("La partie s'est interommpue brutalement.")
            game.send_message_to_all("La partie s'est interommpue brutalement.")
            game.receive = False
            window.destroy()
            exit(-1)

    window.protocol("WM_DELETE_WINDOW", closing)

    def kill_player(player: Player):
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
                main()
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
                main()
            else:
                window.destroy()
        else:
            send_sms(player.phone, "Vous avez été confirmé comme en tant que mort par le maître du jeu !")

    def reborn_player(player: Player):
        player.dead = False
        del game.dead_players[game.dead_players.index(player)]
        if player.role == "impostor":
            game.impostors.append(player)
        else: 
            game.crewmates.append(player)
        show_players()

    playFrame = Frame(window, width=800, height=600, bg="#f5f5f5")

    def show_players():
        clear_frame(playFrame)
        for player in game.players:
            persoFrame = Frame(playFrame, width=800, height=100, bg="#f5f5f5", highlightbackground="#000000",
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

            label_player = Label(persoFrame, text=player.get_str(game), font=("Arial", 20), bg=bg, fg=fg)
            label_player.pack(expand=True, side=LEFT)
            label_player.pack()

            sendMessage = Button(persoFrame, text="Envoyer un message",
                                 command=lambda joueur=player: send_message_window(joueur))
            sendMessage.pack(anchor="e", expand=YES, side=RIGHT)

            taskButton = Button(persoFrame, text="Tâches", command=lambda joueur=player: show_tasks(joueur))
            if not game_master: 
                taskButton.configure(state="disabled")

            if player.finished_all_tasks() and game_master:
                taskButton.config(bg="#00b300")

            taskButton.pack(anchor="e", expand=YES, side=RIGHT)

            deadButton = Button(persoFrame, text="Mort", command=lambda joueur=player: kill_player(joueur))
            if player.dead:
                deadButton.configure(state="disabled")
            deadButton.pack(anchor="e", expand=YES, side=RIGHT)
            persoFrame.pack(fill=BOTH, expand=True)

            rebornButton = Button(persoFrame, text="Réapparaître", command=lambda joueur=player: reborn_player(joueur))
            if not player.dead:
                rebornButton.configure(state="disabled")
            rebornButton.pack(anchor="e", expand=YES, side=RIGHT)
            persoFrame.pack()

        cadavreButton = Button(playFrame, text="Cadavre", command=lambda: game.send_message_to_all(
            "Un cadavre a été signalé.\nMerci de vous rendre immédiatement au point de rendez vous !"))
        cadavreButton.pack(expand=YES, side=RIGHT)
        reunionButton = Button(playFrame, text="Réunion", command=lambda: game.send_message_to_all(
            "Une réunion a été demandée.\nMerci de vous rendre immédiatement au point de rendez vous !"))
        reunionButton.pack(expand=YES, side=LEFT)
        sendAllMessageButton = Button(playFrame, text="Envoyer un message", command=lambda: send_message_all_window())
        sendAllMessageButton.pack(expand=YES, side=LEFT)
        playFrame.pack()

    show_players()

    tasksProgress = Frame(window, width=800, height=100, bg="#f5f5f5")
    label_tasks = Label(tasksProgress, text=f"{len(game.done_tasks)}/{game.given_tasks} tâches données",
                        font=("Arial", 20))
    label_tasks.pack(fill=X, side=BOTTOM)
    tasksProgressBar = ttk.Progressbar(tasksProgress, orient="horizontal", length=800, mode="determinate")
    tasksProgressBar.pack(fill=X, side=BOTTOM)
    tasksProgressBar.config(value=len(game.done_tasks) / game.given_tasks * 100)
    tasksProgress.pack(fill=X, side=BOTTOM)

    def show_tasks(player: Player):
        taskWindow = Tk()
        taskWindow.title(f"Tâches de {player.name} {player.lastname}")
        taskWindow.geometry("500x500")
        taskWindow.resizable(True, True)
        taskWindow.configure(background="white")
        taskWindow.iconbitmap("amongus.ico")
        taskWindow.focus_force()

        tasksFrame = Frame(taskWindow, bg="white")
        tasksFrame.pack(fill=BOTH, expand=True)

        def show_tasks_frame():
            clear_frame(tasksFrame)
            for task in player.tasks:
                taskFrame = Frame(tasksFrame, bg="white")
                if task.done:
                    bg = "#00b300"
                    fg = "#000000"
                else:
                    bg = "#f5f5f5"
                    fg = "#000000"
                taskLabel = Label(taskFrame, text=task.__str__(), bg=bg, fg=fg, font="Arial 10")
                taskLabel.pack(expand=True, side=LEFT)
                taskDoneButton = Button(taskFrame, text="Faite", command=lambda tache=task: task_done(tache))
                taskDoneButton.pack(anchor="e", expand=YES, side=RIGHT)
                taskUndoneButton = Button(taskFrame, text="Non faite", command=lambda tache=task: task_undone(tache))
                taskUndoneButton.pack(anchor="e", expand=YES, side=RIGHT)
                if task.done:
                    taskDoneButton.configure(state="disabled")
                else:
                    taskUndoneButton.configure(state="disabled")
                if player.role == "impostor":
                    taskDoneButton.configure(state="disabled")
                    taskUndoneButton.configure(state="disabled")

                detailsButton = Button(taskFrame, text="Détails", command=lambda tache=task: show_details(tache))
                detailsButton.pack(anchor="e", expand=YES, side=RIGHT)

                taskFrame.pack(fill=BOTH, expand=True)

        show_tasks_frame()

        def task_done(task: Task):
            task.done = True
            game.done_tasks.append(task)
            tasksProgressBar.config(value=len(game.done_tasks) / game.given_tasks * 100)
            label_tasks.config(text=f"{len(game.done_tasks)}/{game.given_tasks} tâches données")
            game.send_messages.append(f"Votre tâche {task.name} a été confirmée comme faite !")
            send_sms(player.phone, f"Votre tâche {task.name} a été confirmée comme faite !")

            if len(game.done_tasks) == game.given_tasks:
                taskWindow.destroy()
                tasksProgressBar.config(value=100)
                game.send_message_to_all(
                    "Les mélenchonnistes ont gagné car ils ont terminé toutes leurs tâches !\nMerci de vous rendre immédiatement au point de rendez vous !")
                response = messagebox.askyesno("Game Over", "Les mélenchonistes ont gagné !\n"
                                                            "Toutes les tâches ont été finies.\n"
                                                            "Voulez-vous recommencer ?")
                if response:
                    window.destroy()
                    main()
                else:
                    window.destroy()
            if player.finished_all_tasks():
                taskWindow.destroy()
                show_players()
                return True
            show_tasks_frame()

        def task_undone(task: Task):
            task.done = False
            del game.done_tasks[game.done_tasks.index(task)]
            tasksProgressBar.config(value=len(game.done_tasks) / game.given_tasks * 100)
            label_tasks.config(text=f"{len(game.done_tasks)}/{game.given_tasks} tâches données")
            show_tasks_frame()

        def show_details(task: Task):
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

        taskWindow.mainloop()

    def send_message_all_window():
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
            message = messageEntry.get()
            game.send_message_to_all(message)
            sender.destroy()

        sendButton = Button(messageFrame, text="Envoyer", command=send_message)
        sendButton.pack(fill=X, expand=YES, side=BOTTOM)

        messageEntry.bind("<Return>", send_message())

        sender.mainloop()

    def send_message_window(player: Player):
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


def clear_frame(frame: Frame):
    """
    Clear all entries in a frame
    :param frame: Frame: Frame to clear
    :return: None
    """
    for widget in frame.winfo_children():
        if widget.winfo_class() == "Frame":
            clear_frame(widget)
        widget.destroy()
