import json
import os
from tkinter import *
from tkinter import messagebox, ttk


def config_config():
    def save_config():
        new_config = {
            "impostors": int(impostorsEntry.get()),
            "ingenors": int(ingenorsEntry.get()),
            "scientists": int(scientistsEntry.get()),
            "tasks": int(tasksEntry.get()),
            "max_task_given": int(maxTaskGivenEntry.get()),
            "ip": ipEntry.get(),
            "names": {
                "impostor": impostorNameEntry.get(),
                "scientist": scientistNameEntry.get(),
                "ingenior": ingeniorNameEntry.get(),
                "crewmate": crewmateNameEntry.get(),
                "title": titleNameEntry.get()
            },
            "max_dead_check": int(maxDeadCheckEntry.get()),
            "game_master": gameMasterEntry.get(),
            "show_dead_roles": showRoleDeadsEntry.get(),
            "discussion_time": int(discussionTimeEntry.get()),
            "vote_time": int(voteTimeEntry.get()),
            "task_list": taskListEntry.get(),
            "manager_type": managerTypeEntry.get(),
            "min_before_inactiv_warn": int(minWarnEntry.get()),
            "max_warns": int(maxWarnsEntry.get())
        }


    window = Tk()
    window.title("Configurer les paramètres")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("amongus.ico")

    with open("config.json", "r", encoding='utf-8') as f:
        config = json.load(f)

    label_title = Label(window, text="Paramètres", font=("Arial", 30))
    label_title.pack(fill=X)

    settingsFrame = Frame(window, bg="#f5f5f5")

    impostorsLabel = Label(settingsFrame, text="Nombre d'imposteurs: ")
    impostorsEntry = Entry(settingsFrame)
    impostorsEntry.insert(0, config["impostors"])
    impostorsLabel.grid(row=0, column=0)
    impostorsEntry.grid(row=0, column=1)

    ingenorsLabel = Label(settingsFrame, text="Nombre d'ingénieurs: ")
    ingenorsEntry = Entry(settingsFrame)
    ingenorsEntry.insert(0, config["ingenors"])
    ingenorsLabel.grid(row=1, column=0)
    ingenorsEntry.grid(row=1, column=1)

    scientistsLabel = Label(settingsFrame, text="Nombre de scientifiques: ")
    scientistsEntry = Entry(settingsFrame)
    scientistsEntry.insert(0, config["scientists"])
    scientistsLabel.grid(row=2, column=0)
    scientistsEntry.grid(row=2, column=1)

    tasksLabel = Label(settingsFrame, text="Nombre de tâches par personne: ")
    tasksEntry = Entry(settingsFrame)
    tasksEntry.insert(0, config["tasks"])
    tasksLabel.grid(row=3, column=0)
    tasksEntry.grid(row=3, column=1)

    maxTaskGivenLabel = Label(settingsFrame, text="Nombre de distribution maximum de la tâche: ")
    maxTaskGivenEntry = Entry(settingsFrame)
    maxTaskGivenEntry.insert(0, config["max_task_given"])
    maxTaskGivenLabel.grid(row=4, column=0)
    maxTaskGivenEntry.grid(row=4, column=1)

    ipLabel = Label(settingsFrame, text="Adresse IP d'Airemore: ")
    ipEntry = Entry(settingsFrame)
    ipEntry.insert(0, config["ip"])
    ipLabel.grid(row=5, column=0)
    ipEntry.grid(row=5, column=1)

    maxDeadCheckLabel = Label(settingsFrame, text="Nombre de consultations pour le scientifique: ")
    maxDeadCheckEntry = Entry(settingsFrame)
    maxDeadCheckEntry.insert(0, config["max_dead_check"])
    maxDeadCheckLabel.grid(row=6, column=0)
    maxDeadCheckEntry.grid(row=6, column=1)

    # TODO: Trouver un autre moyen pour le True/False
    gameMasterLabel = Label(settingsFrame, text="Avec un maître du jeu: ")
    gameMasterEntry = Entry(settingsFrame)
    gameMasterEntry.insert(0, config["game_master"])
    gameMasterLabel.grid(row=7, column=0)
    gameMasterEntry.grid(row=7, column=1)

    # TODO: Trouver un autre moyen pour le True/False
    showRoleDeadsLabel = Label(settingsFrame, text="Dévoiler les rôles après la mort: ")
    showRoleDeadsEntry = Entry(settingsFrame)
    showRoleDeadsEntry.insert(0, config["show_role_deads"])
    showRoleDeadsLabel.grid(row=8, column=0)
    showRoleDeadsEntry.grid(row=8, column=1)

    discussionTimeLabel = Label(settingsFrame, text="Temps de discussions (en secondes): ")
    discussionTimeEntry = Entry(settingsFrame)
    discussionTimeEntry.insert(0, config["discussion_time"])
    discussionTimeLabel.grid(row=9, column=0)
    discussionTimeEntry.grid(row=9, column=1)

    voteTimeLabel = Label(settingsFrame, text="Temps de vote (en secondes): ")
    voteTimeEntry = Entry(settingsFrame)
    voteTimeEntry.insert(0, config["vote_time"])
    voteTimeLabel.grid(row=10, column=0)
    voteTimeEntry.grid(row=10, column=1)

    minWarnLabel = Label(settingsFrame, text="Minutes avant l'avertissement d'inactivité")
    minWarnEntry = Entry(settingsFrame)
    minWarnEntry.insert(0, config["min_warn"])
    minWarnLabel.grid(row=11, column=0)
    minWarnEntry.grid(row=11, column=1)

    maxWarnsLabel = Label(settingsFrame,
                          text="Nombre d'avertissements d'inactivité avant la mise en pause de la partie")
    maxWarnsEntry = Entry(settingsFrame)
    maxWarnsEntry.insert(0, config["max_warns"])
    maxWarnsLabel.grid(row=12, column=0)
    maxWarnsEntry.grid(row=12, column=1)

    # TODO: faire un système de liste
    managerTypeLabel = Label(settingsFrame, text="Type de gestion des joueurs: ")
    managerTypeEntry = Entry(settingsFrame)
    managerTypeEntry.insert(0, config["manager_type"])
    managerTypeLabel.grid(row=11, column=0)
    managerTypeEntry.grid(row=11, column=1)

    # TODO: faire un système de liste
    taskListLabel = Label(settingsFrame, text="Liste de tâches utilisée: ")
    taskListEntry = Entry(settingsFrame)
    taskListEntry.insert(0, config["task_list"])
    taskListLabel.grid(row=12, column=0)
    taskListEntry.grid(row=12, column=1)

    settingsFrame.pack(fill=X)

    ttk.Separator(window, orient="horizontal").pack(fill="x")

    label_names = Label(window, text="Noms des rôles", font=("Arial", 25))
    label_names.pack(fill=X)

    namesFrame = Frame(window, bg="#f5f5f5")

    impostorNameLabel = Label(namesFrame, text="Imposteur: ")
    impostorNameEntry = Entry(namesFrame)
    impostorNameEntry.insert(0, config["names"]["impostor"])
    impostorNameLabel.grid(row=0, column=0)
    impostorNameEntry.grid(row=0, column=1)

    scientistNameLabel = Label(namesFrame, text="Scientifique: ")
    scientistNameEntry = Entry(namesFrame)
    scientistNameEntry.insert(0, config["names"]["scientist"])
    scientistNameLabel.grid(row=1, column=0)
    scientistNameEntry.grid(row=1, column=1)

    ingeniorNameLabel = Label(namesFrame, text="Imposteur: ")
    ingeniorNameEntry = Entry(namesFrame)
    ingeniorNameEntry.insert(0, config["names"]["ingenior"])
    ingeniorNameLabel.grid(row=2, column=0)
    ingeniorNameEntry.grid(row=2, column=1)

    crewmateNameLabel = Label(namesFrame, text="Membre de l'équipe: ")
    crewmateNameEntry = Entry(namesFrame)
    crewmateNameEntry.insert(0, config["names"]["crewmate"])
    crewmateNameLabel.grid(row=3, column=0)
    crewmateNameEntry.grid(row=3, column=1)

    titleNameLabel = Label(namesFrame, text="Nom du jeu: ")
    titleNameEntry = Entry(namesFrame)
    titleNameEntry.insert(0, config["names"]["title"])
    titleNameLabel.grid(row=0, column=0)
    titleNameEntry.grid(row=0, column=1)

    namesFrame.pack(fill=X)

    saveButton = Button(window, text="Enregistrer", command=save_config)
    saveButton.pack(side=BOTTOM)

    window.mainloop()
