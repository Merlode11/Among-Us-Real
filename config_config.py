import json
import os
from tkinter import *
from tkinter import messagebox, ttk


def config_config():
    def save_config(close=False):
        new_config = {
            "impostors": int(impostors_entry.get()),
            "ingeniors": int(ingeniors_entry.get()),
            "scientists": int(scientists_entry.get()),
            "tasks": int(tasks_entry.get()),
            "max_task_given": int(max_task_given_entry.get()),
            "ip": ip_entry.get(),
            "names": {
                "impostor": impostor_name_entry.get(),
                "scientist": scientist_name_entry.get(),
                "ingenior": ingenior_name_entry.get(),
                "crewmate": crewmate_name_entry.get(),
                "title": title_name_entry.get()
            },
            "max_dead_check": int(max_dead_check_entry.get()),
            "game_master": game_master_entry.get(),
            "show_dead_roles": show_role_deads_entry.get(),
            "discussion_time": int(discussion_time_entry.get()),
            "vote_time": int(vote_time_entry.get()),
            "task_list": task_list_entry.get(),
            "manager_type": manager_type_entry.get(),
            "min_before_inactiv_warn": int(min_warn_entry.get()),
            "max_warns": int(max_warns_entry.get())
        }
        with open("config.json", "w", encoding='utf8') as file:
            json.dump(new_config, file, indent=4, ensure_ascii=False)
        messagebox.showinfo("Sauvegarde", "La configuration a été sauvegardée", parent=window)
        if close:
            window.destroy()

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

    settings_frame = Frame(window, bg="#f5f5f5")

    impostors_label = Label(settings_frame, text="Nombre d'imposteurs: ")
    impostors_entry = Entry(settings_frame)
    impostors_entry.insert(0, config["impostors"])
    impostors_label.grid(row=0, column=0)
    impostors_entry.grid(row=0, column=1)

    ingeniors_label = Label(settings_frame, text="Nombre d'ingénieurs: ")
    ingeniors_entry = Entry(settings_frame)
    ingeniors_entry.insert(0, config["ingeniors"])
    ingeniors_label.grid(row=1, column=0)
    ingeniors_entry.grid(row=1, column=1)

    scientists_label = Label(settings_frame, text="Nombre de scientifiques: ")
    scientists_entry = Entry(settings_frame)
    scientists_entry.insert(0, config["scientists"])
    scientists_label.grid(row=2, column=0)
    scientists_entry.grid(row=2, column=1)

    tasks_label = Label(settings_frame, text="Nombre de tâches par personne: ")
    tasks_entry = Entry(settings_frame)
    tasks_entry.insert(0, config["tasks"])
    tasks_label.grid(row=3, column=0)
    tasks_entry.grid(row=3, column=1)

    max_task_given_label = Label(settings_frame, text="Nombre de distribution maximum de la tâche: ")
    max_task_given_entry = Entry(settings_frame)
    max_task_given_entry.insert(0, config["max_task_given"])
    max_task_given_label.grid(row=4, column=0)
    max_task_given_entry.grid(row=4, column=1)

    ip_label = Label(settings_frame, text="Adresse IP d'Airemore: ")
    ip_entry = Entry(settings_frame)
    ip_entry.insert(0, config["ip"])
    ip_label.grid(row=5, column=0)
    ip_entry.grid(row=5, column=1)

    max_dead_check_label = Label(settings_frame, text="Nombre de consultations pour le scientifique: ")
    max_dead_check_entry = Entry(settings_frame)
    max_dead_check_entry.insert(0, config["max_dead_check"])
    max_dead_check_label.grid(row=6, column=0)
    max_dead_check_entry.grid(row=6, column=1)

    # TODO: Trouver un autre moyen pour le True/False
    game_master_label = Label(settings_frame, text="Avec un maître du jeu: ")
    game_master_entry = Entry(settings_frame)
    game_master_entry.insert(0, config["game_master"])
    game_master_label.grid(row=7, column=0)
    game_master_entry.grid(row=7, column=1)

    # TODO: Trouver un autre moyen pour le True/False
    show_role_deads_label = Label(settings_frame, text="Dévoiler les rôles après la mort: ")
    show_role_deads_entry = Entry(settings_frame)
    show_role_deads_entry.insert(0, config["show_dead_roles"])
    show_role_deads_label.grid(row=8, column=0)
    show_role_deads_entry.grid(row=8, column=1)

    discussion_time_label = Label(settings_frame, text="Temps de discussions (en secondes): ")
    discussion_time_entry = Entry(settings_frame)
    discussion_time_entry.insert(0, config["discussion_time"])
    discussion_time_label.grid(row=9, column=0)
    discussion_time_entry.grid(row=9, column=1)

    vote_time_label = Label(settings_frame, text="Temps de vote (en secondes): ")
    vote_time_entry = Entry(settings_frame)
    vote_time_entry.insert(0, config["vote_time"])
    vote_time_label.grid(row=10, column=0)
    vote_time_entry.grid(row=10, column=1)

    min_warn_label = Label(settings_frame, text="Minutes avant l'avertissement d'inactivité")
    min_warn_entry = Entry(settings_frame)
    min_warn_entry.insert(0, config["min_before_inactiv_warn"])
    min_warn_label.grid(row=11, column=0)
    min_warn_entry.grid(row=11, column=1)

    max_warns_label = Label(settings_frame,
                            text="Nombre d'avertissements d'inactivité avant la mise en pause de la partie")
    max_warns_entry = Entry(settings_frame)
    max_warns_entry.insert(0, config["max_warns"])
    max_warns_label.grid(row=12, column=0)
    max_warns_entry.grid(row=12, column=1)

    # TODO: faire un système de liste
    manager_type_label = Label(settings_frame, text="Type de gestion des joueurs: ")
    manager_type_entry = Entry(settings_frame)
    manager_type_entry.insert(0, config["manager_type"])
    manager_type_label.grid(row=13, column=0)
    manager_type_entry.grid(row=13, column=1)

    # TODO: faire un système de liste
    task_list_label = Label(settings_frame, text="Liste de tâches utilisée: ")
    task_list_entry = Entry(settings_frame)
    task_list_entry.insert(0, config["task_list"])
    task_list_label.grid(row=14, column=0)
    task_list_entry.grid(row=14, column=1)

    settings_frame.pack(fill=X)

    ttk.Separator(window, orient="horizontal").pack(fill="x")

    label_names = Label(window, text="Noms des rôles", font=("Arial", 25))
    label_names.pack(fill=X)

    names_frame = Frame(window, bg="#f5f5f5")

    impostor_name_label = Label(names_frame, text="Imposteur: ")
    impostor_name_entry = Entry(names_frame)
    impostor_name_entry.insert(0, config["names"]["impostor"])
    impostor_name_label.grid(row=0, column=0)
    impostor_name_entry.grid(row=0, column=1)

    scientist_name_label = Label(names_frame, text="Scientifique: ")
    scientist_name_entry = Entry(names_frame)
    scientist_name_entry.insert(0, config["names"]["scientist"])
    scientist_name_label.grid(row=1, column=0)
    scientist_name_entry.grid(row=1, column=1)

    ingenior_name_label = Label(names_frame, text="Imposteur: ")
    ingenior_name_entry = Entry(names_frame)
    ingenior_name_entry.insert(0, config["names"]["ingenior"])
    ingenior_name_label.grid(row=2, column=0)
    ingenior_name_entry.grid(row=2, column=1)

    crewmate_name_label = Label(names_frame, text="Membre de l'équipe: ")
    crewmate_name_entry = Entry(names_frame)
    crewmate_name_entry.insert(0, config["names"]["crewmate"])
    crewmate_name_label.grid(row=3, column=0)
    crewmate_name_entry.grid(row=3, column=1)

    title_name_label = Label(names_frame, text="Nom du jeu: ")
    title_name_entry = Entry(names_frame)
    title_name_entry.insert(0, config["names"]["title"])
    title_name_label.grid(row=0, column=0)
    title_name_entry.grid(row=0, column=1)

    names_frame.pack(fill=X)

    save_button = Button(window, text="Enregistrer", command=save_config, width=20)
    save_button.pack(side=BOTTOM)
    save_button_close = Button(window, text="Enregistrer et fermer", command=lambda: save_config(True), width=20)
    save_button_close.pack(side=BOTTOM)

    window.mainloop()
