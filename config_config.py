import json
import os
from tkinter import *
from tkinter import messagebox, ttk

def config_config():
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
    impostorsEntry = Entry(settingsFrame, value=str(config["impostors"]))
    impostorsLabel.grid(0, 0)
    impostorsEntry.grid(0, 1)
    
    ingenorsLabel = Label(settingsFrame, text="Nombre d'ingénieurs: ")
    ingenorsEntry = Entry(settingsFrame, value=str(config["ingenors"]))
    ingenorsLabel.grid(1, 0)
    ingenorsEntry.grid(1, 1)
    
    scientistsLabel = Label(settingsFrame, text="Nombre de scientifiques: ")
    scientistsEntry = Entry(settingsFrame, value=str(config["scientists"]))
    scientistsLabel.grid(2, 0)
    scientistsEntry.grid(2, 1)
    
    tasksLabel = Label(settingsFrame, text="Nombre de tâches par personne: ")
    tasksEntry = Entry(settingsFrame, value=str(config["tasks"]))
    tasksLabel.grid(3, 0)
    tasksEntry.grid(3, 1)
    
    maxTaskGivenLabel = Label(settingsFrame, text="Nombre de distribution maximum de la tâche: ")
    maxTaskGivenEntry = Entry(settingsFrame, value=str(config["max_task_given"]))
    maxTaskGivenLabel.grid(4, 0)
    maxTaskGivenEntry.grid(4, 1)
    
    ipLabel = Label(settingsFrame, text="Adresse IP d'Airemore: ")
    ipEntry = Entry(settingsFrame, value=str(config["ip"]))
    ipLabel.grid(5, 0)
    ipEntry.grid(5, 1)
    
    maxDeadCheckLabel = Label(settingsFrame, text="Nombre de consultations pour le scientifique: ")
    maxDeadCheckEntry = Entry(settingsFrame, value=str(config["max_dead_check"]))
    maxDeadCheckLabel.grid(6, 0)
    maxDeadCheckEntry.grid(6, 1)
    
    # TODO: Trouver un autre moyen pour le True/False
    gameMasterLabel = Label(settingsFrame, text="Avec un maître du jeu: ")
    gameMasterEntry = Entry(settingsFrame, value=str(config["game_master"]))
    gameMasterLabel.grid(7, 0)
    gameMasterEntry.grid(7, 1)
    
    # TODO: Trouver un autre moyen pour le True/False
    showRoleDeadsLabel = Label(settingsFrame, text="Dévoiler les rôles après la mort: ")
    showRoleDeadsEntry = Entry(settingsFrame, value=str(config["show_dead_roles"]))
    showRoleDeadsLabel.grid(8, 0)
    showRoleDeadsEntry.grid(8, 1)
    
    discussionTimeLabel = Label(settingsFrame, text="Temps de discussions (en secondes): ")
    discussionTimeEntry = Entry(settingsFrame, value=str(config["discussion_time"]))
    discussionTimeLabel.grid(9, 0)
    discussionTimeEntry.grid(9, 1)
    
    voteTimeLabel = Label(settingsFrame, text="Temps de vote (en secondes): ")
    voteTimeEntry = Entry(settingsFrame, value=str(config["vote_time"]))
    voteTimeLabel.grid(10, 0)
    voteTimeEntry.grid(10, 1)
    
    # TODO: faire un système de liste
    managerTypeLabel = Label(settingsFrame, text="Type de gestion des joueurs: ")
    managerTypeEntry = Entry(settingsFrame, value=str(config["manager_type"]))
    managerTypeLabel.grid(11, 0)
    managerTypeEntry.grid(11, 1)
    
    # TODO: faire un système de liste
    taskListLabel = Label(settingsFrame, text="Nombre de tâches par personne: ")
    taskListEntry = Entry(settingsFrame, value=str(config["task_list"]))
    taskListLabel.grid(12, 0)
    taskListEntry.grid(12, 1)
    
    settingsFrame.pack(fill=X)
    
    ttk.Separator(window, orient="horizontal").pack(fill="x")
    
    label_names = Label(window, text="Noms des rôles", font=("Arial", 25))
    label_names.pack(fill=X)
    
    namesFrame = Frame(window, bg="#f5f5f5")
    
    impostorNameLabel = Label(namesFrame, text="Imposteur: ")
    impostorNameEntry = Entry(namesFrame, value=str(config["names"]["impostor"]))
    impostorNameLabel.grid(0, 0)
    impostorNameEntry.grid(0, 1)
    
    scientistNameLabel = Label(namesFrame, text="Scientifique: ")
    scientistNameEntry = Entry(namesFrame, value=str(config["names"]["scientist"]))
    scientistNameLabel.grid(1, 0)
    scientistNameEntry.grid(1, 1)
    
    ingeniorNameLabel = Label(namesFrame, text="Imposteur: ")
    ingeniorNameEntry = Entry(namesFrame, value=str(config["names"]["ingenior"]))
    ingeniorNameLabel.grid(2, 0)
    ingeniorNameEntry.grid(2, 1)
    
    crewmateNameLabel = Label(namesFrame, text="Membre de l'équipe: ")
    crewmateNameEntry = Entry(namesFrame, value=str(config["names"]["crewmate"]))
    crewmateNameLabel.grid(3, 0)
    crewmateNameEntry.grid(3, 1)
    
    titleNameLabel = Label(namesFrame, text="Nom du jeu: ")
    titleNameEntry = Entry(namesFrame, value=str(config["names"]["title"]))
    titleNameLabel.grid(0, 0)
    titleNameEntry.grid(0, 1)
    
    namesFrame.pack(fill=X)
    
    saveButton = Button(window, text="Enregistrer", command=save_config)
    saveButton.pack(side=BOTTOM)
    
    window.mainloop()
    
    def save_config(): 
        
