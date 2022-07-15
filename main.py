#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
from tkinter import *
from tkinter import messagebox, ttk
from smsManager import send_sms, get_new_messages


class Player:
    def __init__(self, name: str, lastname: str, phone: str):
        self.name: str = name
        self.lastname: str = lastname
        self.phone: str = phone
        self.tasks: list = []
        self.role: str = ""
        self.dead: bool = False
        self.asks: int = 0

    def __repr__(self):
        if self.dead:
            return f"☠ {self.name} {self.lastname} ({self.role}): {self.phone}"
        return f"{self.name} {self.lastname} ({self.role}): {self.phone}"

    def finished_all_tasks(self):
        finished = 0
        for task in self.tasks:
            if task.done:
                finished += 1
        return finished == len(self.tasks)


class Task:
    def __init__(self, name: str, description: str, classe: str, location: str, other: dict = None):
        self.name: str = name
        self.description: str = description
        self.classe: str = classe
        self.location: str = location
        self.done: bool = False
        self.other: dict = other
        self.nb_given: int = 0
        self.success: int = 0

    def __repr__(self):
        return f"{self.name} ({self.classe}): {self.description} | {self.location}"

    def __str__(self):
        return f"{self.name} ({self.classe})"


class Game:
    def __init__(self):
        with open("players-exemple.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            self.players = [Player(player["name"], player["lastname"], player["phone"]) for player in data if
                            player.get("play") is None]

        self.tasks: list = []
        with open(r"tasks.json", "r", encoding='utf-8') as f:
            data = json.load(f)
            self.tasks = [Task(task["name"], task["description"], task["type"], task["location"], task.get("other")) for
                          task in data]
        self.given_tasks: int = 0

        self.crewmates: list = []
        self.impostors: list = []
        self.dead_players: list = []
        self.done_tasks: list = []
        self.receive: bool = True
        self.send_messages: list = []

        with open("config.json", "r", encoding='utf-8') as f:
            self.config = json.load(f)

    def define_roles(self):
        random.shuffle(self.players)
        for i in range(self.config["impostors"]):
            self.impostors.append(self.players[i])
            self.players[i].role = self.config["names"]["impostor"]
        self.crewmates = self.players[self.config["impostors"]:]

        for player in self.crewmates:
            player.role = self.config["names"]["crewmate"]
        for player in self.impostors:
            player.role = self.config["names"]["impostor"]

        for i in range(self.config["ingenors"]):
            self.crewmates[i].role = self.config["names"]["ingenior"]
        for i in range(self.config["scientists"]):
            self.crewmates[i + self.config["ingenors"]].role = self.config["names"]["scientist"]

        self.players = sorted(self.players, key=lambda joueur: joueur.name)

    def define_tasks(self):
        for player in self.players:
            random.shuffle(self.tasks)
            for i in range(self.config["tasks"]):
                player.tasks.append(Task(self.tasks[i].name, self.tasks[i].description, self.tasks[i].classe,
                                         self.tasks[i].location, self.tasks[i].other))
                self.tasks[i].nb_given += 1
                if self.tasks[i].nb_given >= self.config["max_given"]:
                    del self.tasks[i]
            if player.role != self.config["names"]["impostor"]:
                self.given_tasks += self.config["tasks"]
            message = f"Bonjour {player.name} {player.lastname},\n"
            message += "Vous êtes un " + player.role.upper()
            if player.role == self.config["names"]["impostor"]:
                impostors = " ".join([(joueur.name + " " + joueur.lastname) for joueur in self.impostors])
                message += " avec " + impostors + "\n\n"
            else:
                message += "\n\n"
            message += "Vos tâches sont:\n"
            for i in range(len(player.tasks)):
                task = player.tasks[i]
                message += f"{i + 1}: {task.name} ({task.classe})\n"
            message += "\n"
            message += "Pour voir toutes les commandes, vous pouvez taper \"help\"\n"
            message += "Nous vous souhaitons une bonne partie !"

            self.send_messages.append(message)
            # send_sms(player.phone, message)

    def send_message_to_all(self, message: str):
        for player in self.players:
            self.send_messages.append(message)
            send_sms(player.phone, message)

        messagebox.showinfo("Succès", "Le message a été envoyé à tout le monde !")

    def check_command(self, player, message):
        message = message.lower()
        if message.startswith(("tâche", "détail", "detail", "task", "tache")):
            try:
                task_number = int(message.split(" ")[1])
                task = player.tasks[task_number - 1]
                string = f"{task.name} ({task.classe})\n"
                string += f"Lieu: {task.location}\n"
                string += f"Description: {task.description}\n"
                self.send_messages.append(string)
                send_sms(player.phone, string)
            except:
                self.send_messages.append("Veuillez entrer un numéro de tâche valide !")
                send_sms(player.phone, "Veuillez entrer un numéro de tâche valide !")
            return True
        elif message.startswith(("info", "restant", "last", "reste")):
            remining = 0
            done = 0
            string = ""
            for i in range(len(player.tasks)):
                task = player.tasks[i]
                if task.done:
                    done += 1
                else:
                    remining += 1
                    string += f"{i + 1}: {task.name} ({task.classe})\n"
            string = f"Il vous reste {remining} tâches à accomplir.\n" + string
            if done == len(player.tasks):
                string += "Vous avez accompli toutes vos tâches !\n"

            string += f"Il reste {len(self.done_tasks)}/{self.given_tasks} tâche pour les mélenchonistes."

            self.send_messages.append(string)
            send_sms(player.phone, string)
            return True
        elif message.startswith(("view", "states", "états", "deads", "morts")):
            if player.role != self.config["names"]["scientist"]:
                self.send_messages.append("Vous ne pouvez pas utiliser cette commande, vous n'êtes pas " + self.config["names"]["scientist"] + " !")
                send_sms(player.phone, "Vous ne pouvez pas utiliser cette commande, vous n'êtes pas " + self.config["names"]["scientist"] + " !")
            elif player.asks >= self.config["max_dead_check"]:
                self.send_messages.append("Vous avez utilisé toutes vos demandes !")
                send_sms(player.phone, "Vous avez utilisé toutes vos demandes !")
            else:
                states = "Voici les états de chaque joueur:\n"
                for joueur in self.players:
                    if joueur.dead:
                        states += "- " + joueur.name + " " + joueur.lastname + " (mort)\n"
                    else:
                        states += "- " + joueur.name + " " + joueur.lastname + " (vivant)\n"
                player.asks += 1
                states += "\n Il vous reste " + str(self.config["max_dead_check"] - player.asks) + "/" + str(self.config["max_dead_check"]) + " demandes."
                self.send_messages.append(states)
                send_sms(player.phone, states)
            return True

        elif message.startswith(("mort", "death", "cadavre", "corps")):
            response = messagebox.askokcancel("Mort détecté",
                                              f"{player.name} {player.lastname} découvert un corps ! Son message est :\n {message}")
            if response == "ok":
                self.send_message_to_all(
                    "Un cadavre a été signalé.\nMerci de vous rendre immédiatement au point de rendez vous !")
            elif response == "cancel":
                self.send_messages.append(f"Votre demande a été refusée par l'organisateur.ice")
                send_sms(player.phone, "Votre demande a été refusée par l'organisateur.ice")
            return True
        elif "chapelure" in message:
            task = next((x for x in player.tasks if x.name == "Le code de la boîte"), None)
            if task is None:
                self.send_messages.append("Vous n'avez pas de tâche de ce type !")
                send_sms(player.phone, "Vous n'avez pas de tâche de ce type !")
                messagebox.showinfo("Erreur",
                                    f"{player.name} {player.lastname} a confirmé avoir réalisé la tâche Le code de la boîte mais il ne possède pas cette tâche !")
                return True
            task.done = True
            self.done_tasks.append(task)
            self.send_messages.append(f"Votre tâche {task.name} a été confirmée comme faite !")
            send_sms(player.phone, f"Votre tâche {task.name} a été confirmée comme faite !")
            messagebox.showinfo("Succès",
                                f"{player.name} {player.lastname} a confirmé avoir réalisé la tâche {task.name} ! Son message est :\n {message}")

            return True
        elif "2.37" in message or "2,37" in message:
            task = next((x for x in player.tasks if x.name == "Mathématiques"), None)
            if task is None:
                self.send_messages.append("Vous n'avez pas de tâche de ce type !")
                send_sms(player.phone, "Vous n'avez pas de tâche de ce type !")
                messagebox.showinfo("Erreur",
                                    f"{player.name} {player.lastname} a confirmé avoir réalisé la tâche Mathématiques mais il ne possède pas cette tâche !")
                return True
            task.done = True
            self.done_tasks.append(task)
            self.send_messages.append(f"Votre tâche {task.name} a été confirmée comme faite !")
            send_sms(player.phone, f"Votre tâche {task.name} a été confirmée comme faite !")
            messagebox.showinfo("Succès",
                                f"{player.name} {player.lastname} a confirmé avoir réalisé la tâche {task.name} ! Son message est :\n {message}")
            return True
        elif message.startswith(("done", "fait", "réalisé")):
            try:
                task_number = int(message.split(" ")[1])
                task = player.tasks[task_number - 1]
                if task.done:
                    self.send_messages.append("Vous avez déjà déclaré avoir fait la tâche " + str(task_number))
                    send_sms(player.phone, "Vous avez déjà déclaré avoir fait la tâche " + str(task_number))
                else:
                    task.done = True
                    self.done_tasks.append(task)
                    self.send_messages.append(f"Votre tâche {task.name} a été confirmée comme faite !")
                    send_sms(player.phone, f"Votre tâche {task.name} a été confirmée comme faite !")
                    messagebox.showinfo("Succès",
                                        f"{player.name} {player.lastname} a confirmé avoir réalisé la tâche {task.name} ! Son message est :\n {message}")
            except:
                self.send_messages.append("Veuillez entrer un numéro de tâche valide !")
                send_sms(player.phone, "Veuillez entrer un numéro de tâche valide !")
            return True
        elif message.startswith(("help", "aide")):
            string = "Voici toutes les commandes disponibles:\n"
            string += "tâche NOMBRE: Permet de voir la description d'une tâche\n"
            string += "info: Permet de voir les tâches restantes\n"
            string += "mort PERSONNE: Annonce à l'organisateur la découverte d'un corps\n"
            string += "fait NOMBRE: Valide une tâche comme faite\n"
            string += "view: Voir les états de chacun"
            self.send_messages.append(string)
            send_sms(player.phone, string)
            return True
        return False

    def start_recieve_sms(self):
        from threading import Timer

        def test():
            new = get_new_messages(self.players)
            if len(new) > 0:
                for msg in new:
                    if msg.content in self.send_messages:
                        del self.send_messages[self.send_messages.index(msg.content)]
                        continue
                    joueur = next((joueur for joueur in self.players if joueur.phone == msg.phone), None)
                    if self.check_command(joueur, msg.content):
                        continue
                    string = "Nouveau message de " + joueur.name + " " + joueur.lastname + " (" + joueur.phone + ") :\n"
                    string += msg.content
                    messagebox.showinfo(f"Message de {msg.phone}", string)
            if self.receive:
                Timer(2, test).start()

        test()


def main():
    game = Game()

    window = Tk()
    window.title("Among Us La Chapelle")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("amongus.ico")
    window.state("zoomed")

    label_title = Label(window, text="Among Us La Chapelle", font=("Arial", 30))
    label_title.pack(fill=X)

    messagebox.showinfo("Bienvenue", "Bienvenue dans le jeu Among Us La Chapelle.\n"
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
        if player.role == game.config["names"]["crewmate"] or player.role == game.config["names"]["ingenior"] or player.role == game.config["names"]["scientist"]:
            del game.crewmates[game.crewmates.index(player)]
        elif player.role == game.config["names"]["impostor"]:
            del game.impostors[game.impostors.index(player)]
        send_sms(player.phone, "Vous avez été confirmé comme en tant que mort par le maître du jeu !")
        show_players()

        if len(game.crewmates) <= len(game.impostors):
            game.send_message_to_all(
                "Tout les " + game.config["names"]["crewmate"].lower() + " sont morts, les " + game.config["names"][
                    "impostor"].lower() + " ont gagné !\nMerci de vous rendre immédiatement au point de rendez-vous !\n")
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

    def reborn_player(player: Player):
        player.dead = False
        del game.dead_players[game.dead_players.index(player)]
        if player.role == game.config["names"]["crewmate"]:
            game.crewmates.append(player)
        elif player.role == game.config["names"]["impostor"]:
            game.impostors.append(player)
        show_players()

    playFrame = Frame(window, width=800, height=600, bg="#f5f5f5")

    def show_players():
        clear_frame(playFrame)
        for player in game.players:
            persoFrame = Frame(playFrame, width=800, height=100, bg="#f5f5f5", highlightbackground="#000000",
                               highlightthickness=1)
            bg = "#a9a9a9" if player.dead else "#f5f5f5"
            fg = "#000000"
            if player.role == game.config["names"]["crewmate"]:
                fg = "#00b300"
            elif player.role == game.config["names"]["impostor"]:
                fg = "#ff0000"
            elif player.role == game.config["names"]["ingenior"]:
                fg = "#ffa500"
            elif player.role == game.config["names"]["scientist"]:
                fg = "#0000ff"

            label_player = Label(persoFrame, text=player.__repr__(), font=("Arial", 20), bg=bg, fg=fg)
            label_player.pack(expand=True, side=LEFT)
            label_player.pack()

            sendMessage = Button(persoFrame, text="Envoyer un message",
                                 command=lambda joueur=player: send_message_window(joueur))
            sendMessage.pack(anchor="e", expand=YES, side=RIGHT)

            taskButton = Button(persoFrame, text="Tâches", command=lambda joueur=player: show_tasks(joueur))

            if player.finished_all_tasks():
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
                if player.role == game.config["names"]["impostor"]:
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

                random.shuffle(task.other["questions"])
                for i in range(3):
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


if __name__ == "__main__":
    main()
