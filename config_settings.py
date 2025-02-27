import json
import os
import re
from tkinter import *
from tkinter import messagebox, ttk
from utils import YesNoButton, VerticalScrolledFrame, IntEntry, TimerEntry
from check_devices import find_sms_ip


def config_settings():
    """
    Affiche la fenêtre de configuration des paramètres
    """

    def save_config(close: bool = False):
        """
        Sauvegarde la configuration dans le fichier JSON de configuration
        :param close: bool: True si la fenêtre doit être fermée après la sauvegarde
        """
        manager_type_str = manager_type.get()
        ip = ip_entry.get()
        discord_token = discord_token_entry.get()
        telegram_token = telegram_token_entry.get()
        if manager_type_str == "sms":
            if not ip.count(".") == 3:
                messagebox.showerror("Erreur", "L'adresse IP n'est pas valide", parent=window)
                ip_entry.focus()
                return
            for i in ip.split("."):
                if not i.isdigit():
                    messagebox.showerror("Erreur", "L'adresse IP n'est pas valide", parent=window)
                    ip_entry.focus()
                    return
                if not 0 <= int(i) <= 255:
                    messagebox.showerror("Erreur", "L'adresse IP n'est pas valide", parent=window)
                    ip_entry.focus()
                    return
        elif manager_type_str == "discord":
            if discord_token == "":
                messagebox.showerror("Erreur",
                                     "Merci de bien vouloir entrer un token de bot Discord pour une utilisation de ce mode de jeu",
                                     parent=window)
                discord_token_entry.focus()
                return
            elif not re.match(r"[A-Za-z\d]{24,28}\.[\w-]{6}\.[\w-]{27,38}", discord_token):
                messagebox.showerror("Erreur",
                                     "Merci de bien vouloir entrer un token de bot Discord valide pour ce mode de jeu",
                                     parent=window)
                discord_token_entry.focus()
                return
        elif manager_type_str == "telegram":
            if telegram_token == "":
                messagebox.showerror("Erreur",
                                     "Merci de bien vouloir entrer un token de bot Telegram pour ce mode de jeu",
                                     parent=window)
                telegram_token_entry.focus()
                return
        elif manager_type_str == "instagram":
            if insta_username_entry.get() == "":
                messagebox.showerror("Erreur",
                                     "Merci de bien vouloir entrer un nom d'utilisateur Instagram pour ce mode de jeu",
                                     parent=window)
                insta_username_entry.focus()
                return
            if insta_password_entry.get() == "":
                messagebox.showerror("Erreur",
                                     "Merci de bien vouloir entrer un mot de passe Instagram correspondant pour ce mode de jeu",
                                     parent=window)
                insta_password_entry.focus()
                return

        new_config: dict = {
            "impostors": int(impostors_entry.get_value()),
            "engineers": int(engineers_entry.get_value()),
            "scientists": int(scientists_entry.get_value()),
            "tasks": int(tasks_entry.get_value()),
            "max_task_given": int(max_task_given_entry.get_value()),
            "names": {
                "impostor": impostor_name_entry.get(),
                "scientist": scientist_name_entry.get(),
                "engineer": engineer_name_entry.get(),
                "crewmate": crewmate_name_entry.get(),
                "title": title_name_entry.get()
            },
            "max_dead_check": int(max_dead_check_entry.get_value()),
            "game_master": game_master_entry.get_value(),
            "show_dead_roles": show_role_deads_entry.get_value(),
            "discussion_time": int(discussion_time_entry.get_total_seconds()),
            "vote_time": int(vote_time_entry.get_total_seconds()),
            "kill_cooldown": int(kill_cooldown_entry.get_total_seconds()),
            "task_list": tasks_list.get(),
            "min_before_inactiv_warn": int(min_warn_entry.get_value()),
            "max_warns": int(max_warns_entry.get_value()),
            "manager_type": manager_type_str,
            "register_type": register_type.get(),
            "save_register": save_register_entry.get_value(),
            "ip": ip,
            "port": port_entry.get_value(),
            "sms_username": sms_username_entry.get(),
            "sms_password": sms_password_entry.get(),
            "discord_token": discord_token,
            "telegram_token": telegram_token,
            "insta_username": insta_username_entry.get(),
            "insta_password": insta_password_entry.get(),
        }
        with open("config.json", "w", encoding='utf8') as file:
            json.dump(new_config, file, indent=4, ensure_ascii=False)
        messagebox.showinfo("Sauvegarde", "La configuration a été sauvegardée", parent=window)
        if close:
            window.destroy()

    def found_ip():
        """
        Affiche l'adresse IP trouvée par le script de recherche d'adresse IP
        """
        # Show a loading animation while the script is running
        founded_ip_window = Toplevel(window)
        founded_ip_window.title("Adresses IP trouvées")
        founded_ip_window.resizable(False, False)
        founded_ip_window.grab_set()

        loading_label = Label(founded_ip_window, text="Recherche en cours...")
        loading_label.pack(pady=10)

        loading_bar = ttk.Progressbar(founded_ip_window, orient=HORIZONTAL, length=200, mode="indeterminate")
        loading_bar.pack(pady=10)
        founded_ip_window.update()
        loading_bar.start(5)

        loading_label.update()

        port = port_entry.get_value()
        ips = find_sms_ip(port)

        if len(ips) == 0:
            messagebox.showinfo("Fin", "Aucune adresse IP n'a été trouvée", parent=founded_ip_window)
            founded_ip_window.destroy()
        elif len(ips) == 1:
            ip_entry.delete(0, END)
            ip_entry.insert(0, ips[0])
            founded_ip_window.destroy()
        else:
            ip_list = Listbox(founded_ip_window, width=20, height=10)
            ip_list.pack()
            for ip in ips:
                ip_list.insert(END, ip)

            def select_ip():
                ip_entry.delete(0, END)
                ip_entry.insert(0, ip_list.get(ACTIVE))
                founded_ip_window.destroy()

            Button(founded_ip_window, text="Sélectionner", command=select_ip).pack(pady=10)
            founded_ip_window.bind("<Return>", lambda event: select_ip())
            founded_ip_window.bind("<Escape>", lambda event: founded_ip_window.destroy())
            founded_ip_window.mainloop()

    window = Tk()
    window.title("Configurer les paramètres")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("assets/img/amongus.ico")

    with open("config.json", "r", encoding='utf-8') as f:
        config = json.load(f)

    with open("players.json", "r", encoding='utf-8') as f:
        players = [player for player in json.load(f) if player.get("play")]

    def set_recommended_imposters():
        impostors_entry.set_value(int(0.4927 + 0.2481 * len(players)))

    label_title = Label(window, text="Paramètres", font=("Arial", 30))
    label_title.pack(fill=X)

    frame = VerticalScrolledFrame(window)

    settings_frame = Frame(frame, bg="#f5f5f5")

    row_num = 0

    # Nombre d'imposteurs:
    impostors_label = Label(settings_frame, text="Nombre d'imposteurs: ")
    impostors_entry = IntEntry(settings_frame, value=config.get("impostors", 1), min_value=1, max_value=10)
    impostors_entry.set_value(config.get("impostors", 1))
    impostors_recommanded_button = Button(settings_frame, text="Définir le nombre recommandé",
                                          command=set_recommended_imposters)
    impostors_label.grid(row=row_num, column=0)
    impostors_entry.grid(row=row_num, column=1)
    impostors_recommanded_button.grid(row=row_num, column=2)
    row_num += 1

    engineers_label = Label(settings_frame, text="Nombre d'ingénieurs: ")
    engineers_entry = IntEntry(settings_frame)
    engineers_entry.set_value(config.get("engineers", 1))
    engineers_label.grid(row=row_num, column=0)
    engineers_entry.grid(row=row_num, column=1)
    row_num += 1

    scientists_label = Label(settings_frame, text="Nombre de scientifiques: ")
    scientists_entry = IntEntry(settings_frame)
    scientists_entry.set_value(config.get("scientists", 1))
    scientists_label.grid(row=row_num, column=0)
    scientists_entry.grid(row=row_num, column=1)
    row_num += 1

    tasks_label = Label(settings_frame, text="Nombre de tâches par personne: ")
    tasks_entry = IntEntry(settings_frame)
    tasks_entry.set_value(config.get("tasks", 1))
    tasks_label.grid(row=row_num, column=0)
    tasks_entry.grid(row=row_num, column=1)
    row_num += 1

    max_task_given_label = Label(settings_frame, text="Nombre de distribution maximum de la tâche: ")
    max_task_given_entry = IntEntry(settings_frame)
    max_task_given_entry.set_value(config.get("max_task_given", 1))
    max_task_given_label.grid(row=row_num, column=0)
    max_task_given_entry.grid(row=row_num, column=1)
    row_num += 1

    max_dead_check_label = Label(settings_frame, text="Nombre de consultations pour le scientifique: ")
    max_dead_check_entry = IntEntry(settings_frame)
    max_dead_check_entry.set_value(config.get("max_dead_check", 1))
    max_dead_check_label.grid(row=row_num, column=0)
    max_dead_check_entry.grid(row=row_num, column=1)
    row_num += 1

    game_master_label = Label(settings_frame, text="Avec un maître du jeu: ")
    game_master_entry = YesNoButton(settings_frame, value=config.get("game_master", False))
    game_master_label.grid(row=row_num, column=0)
    game_master_entry.grid(row=row_num, column=1)
    row_num += 1

    show_role_deads_label = Label(settings_frame, text="Dévoiler les rôles après la mort: ")
    show_role_deads_entry = YesNoButton(settings_frame, value=config.get("show_dead_roles", False))
    show_role_deads_label.grid(row=row_num, column=0)
    show_role_deads_entry.grid(row=row_num, column=1)
    row_num += 1

    discussion_time_label = Label(settings_frame, text="Temps de discussions: ")
    discussion_time_entry = TimerEntry(settings_frame)
    discussion_time_entry.set_total_seconds(config.get("discussion_time", 0))
    discussion_time_label.grid(row=row_num, column=0)
    discussion_time_entry.grid(row=row_num, column=1)
    row_num += 1

    vote_time_label = Label(settings_frame, text="Temps de vote: ")
    vote_time_entry = TimerEntry(settings_frame)
    vote_time_entry.set_total_seconds(config.get("vote_time", 0))
    vote_time_label.grid(row=row_num, column=0)
    vote_time_entry.grid(row=row_num, column=1)
    row_num += 1

    kill_cooldown_label = Label(settings_frame, text="Temps entre les assassinats: ")
    kill_cooldown_entry = TimerEntry(settings_frame)
    kill_cooldown_entry.set_total_seconds(config.get("kill_cooldown", 0))
    kill_cooldown_label.grid(row=row_num, column=0)
    row_num += 1

    min_warn_label = Label(settings_frame, text="Minutes avant l'avertissement d'inactivité")
    min_warn_entry = IntEntry(settings_frame)
    min_warn_entry.set_value(config.get("min_before_inactiv_warn", 0))
    min_warn_label.grid(row=row_num, column=0)
    min_warn_entry.grid(row=row_num, column=1)
    row_num += 1

    max_warns_label = Label(settings_frame,
                            text="Nombre d'avertissements d'inactivité avant la mise en pause de la partie")
    max_warns_entry = IntEntry(settings_frame)
    max_warns_entry.set_value(config.get("max_warns", 0))
    max_warns_label.grid(row=row_num, column=0)
    max_warns_entry.grid(row=row_num, column=1)
    row_num += 1

    manager_type = StringVar()
    manager_type.set(config.get("manager_type", "web"))
    manager_type_label = Label(settings_frame, text="Type de gestion des joueurs: ")
    manager_type_entry = OptionMenu(settings_frame, manager_type,
                                    *["sms", "web", "whatsapp", "instagram", "discord", "telegram"])
    manager_type_label.grid(row=row_num, column=0)
    manager_type_entry.grid(row=row_num, column=1)
    row_num += 1

    port_label = Label(settings_frame, text="Port d'SMS-gate (vide si non utilisé): ")
    port_entry = IntEntry(settings_frame, value=config.get("port", 8080), min_value=1023, max_value=65535)
    port_label.grid(row=row_num, column=0)
    port_entry.grid(row=row_num, column=1)
    row_num += 1

    ip_label = Label(settings_frame, text="Adresse IP d'SMS-gate (vide si non utilisé): ")
    ip_entry = Entry(settings_frame)
    ip_entry.insert(0, config.get("ip", ""))
    foud_ip_button = Button(settings_frame, text="Trouver l'adresse IP", command=found_ip)
    ip_label.grid(row=row_num, column=0)
    ip_entry.grid(row=row_num, column=1)
    foud_ip_button.grid(row=row_num, column=2)
    row_num += 1

    sms_username_label = Label(settings_frame, text="Nom d'utilisateur SMS-gate: ")
    sms_username_entry = Entry(settings_frame)
    sms_username_entry.insert(0, config.get("sms_username", ""))
    sms_username_label.grid(row=row_num, column=0)
    sms_username_entry.grid(row=row_num, column=1)
    row_num += 1

    sms_password_label = Label(settings_frame, text="Mot de passe SMS-gate: ")
    sms_password_entry = Entry(settings_frame)
    sms_password_entry.insert(0, config.get("sms_password", ""))
    sms_password_label.grid(row=row_num, column=0)
    sms_password_entry.grid(row=row_num, column=1)
    row_num += 1

    discord_token_label = Label(settings_frame, text="Token du bot Discord: ")
    discord_token_entry = Entry(settings_frame)
    discord_token_entry.insert(0, config.get("discord_token", ""))
    discord_token_label.grid(row=row_num, column=0)
    discord_token_entry.grid(row=row_num, column=1)
    row_num += 1

    telegram_token_label = Label(settings_frame, text="Token du bot Telegram: ")
    telegram_token_entry = Entry(settings_frame)
    telegram_token_entry.insert(0, config.get("telegram_token", ""))
    telegram_token_label.grid(row=row_num, column=0)
    telegram_token_entry.grid(row=row_num, column=1)
    row_num += 1

    insta_username_label = Label(settings_frame, text="Nom d'utilisateur Instagram: ")
    insta_username_entry = Entry(settings_frame)
    insta_username_entry.insert(0, config.get("insta_username", ""))
    insta_username_label.grid(row=row_num, column=0)
    insta_username_entry.grid(row=row_num, column=1)
    row_num += 1

    insta_password_label = Label(settings_frame, text="Mot de passe instagram: ")
    insta_password_entry = Entry(settings_frame)
    insta_password_entry.insert(0, config.get("insta_password", ""))
    insta_password_label.grid(row=row_num, column=0)
    insta_password_entry.grid(row=row_num, column=1)
    row_num += 1

    register_type = StringVar()
    register_type.set(config.get("register_type", "liste"))
    register_type_label = Label(settings_frame, text="Type de définition des joueurs: ")
    register_type_entry = OptionMenu(settings_frame, register_type, *["liste", "direct"])
    register_type_label.grid(row=row_num, column=0)
    register_type_entry.grid(row=row_num, column=1)
    row_num += 1

    save_register_label = Label(settings_frame,
                                text="Si la définition est directe, enregistrer dans une liste pour plus tard: ")
    save_register_entry = YesNoButton(settings_frame, value=config.get("save_register", False))
    save_register_label.grid(row=row_num, column=0)
    save_register_entry.grid(row=row_num, column=1)
    row_num += 1

    tasks = [liste.replace(".json", "") for liste in os.listdir("taskList") if liste.endswith(".json")]
    if config.get("tasks", "") not in tasks:
        config["tasks"] = tasks[0]
    tasks_list = StringVar()
    tasks_list.set(config.get("tasks", ""))
    task_list_label = Label(settings_frame, text="Liste de tâches utilisée: ")
    task_list_entry = OptionMenu(settings_frame, tasks_list, *tasks)
    task_list_label.grid(row=row_num, column=0)
    task_list_entry.grid(row=row_num, column=1)
    row_num += 1

    settings_frame.pack(fill=X)

    ttk.Separator(frame, orient="horizontal").pack(fill="x")

    label_names = Label(frame, text="Noms des rôles", font=("Arial", 25))
    label_names.pack(fill=X)

    names_frame = Frame(frame, bg="#f5f5f5")

    row_num = 0

    impostor_name_label = Label(names_frame, text="Imposteur: ")
    impostor_name_entry = Entry(names_frame)
    impostor_name_entry.insert(0, config.get("names", {}).get("impostor", ""))
    impostor_name_label.grid(row=row_num, column=0)
    impostor_name_entry.grid(row=row_num, column=1)
    row_num += 1

    scientist_name_label = Label(names_frame, text="Scientifique: ")
    scientist_name_entry = Entry(names_frame)
    scientist_name_entry.insert(0, config.get("names", {}).get("scientist", ""))
    scientist_name_label.grid(row=row_num, column=0)
    scientist_name_entry.grid(row=row_num, column=1)
    row_num += 1

    engineer_name_label = Label(names_frame, text="Ingénieur: ")
    engineer_name_entry = Entry(names_frame)
    engineer_name_entry.insert(0, config.get("names", {}).get("engineer", ""))
    engineer_name_label.grid(row=row_num, column=0)
    engineer_name_entry.grid(row=row_num, column=1)
    row_num += 1

    crewmate_name_label = Label(names_frame, text="Membre de l'équipe: ")
    crewmate_name_entry = Entry(names_frame)
    crewmate_name_entry.insert(0, config.get("names", {}).get("crewmate", ""))
    crewmate_name_label.grid(row=row_num, column=0)
    crewmate_name_entry.grid(row=row_num, column=1)
    row_num += 1

    title_name_label = Label(names_frame, text="Nom du jeu: ")
    title_name_entry = Entry(names_frame)
    title_name_entry.insert(0, config.get("names", {}).get("title", ""))
    title_name_label.grid(row=row_num, column=0)
    title_name_entry.grid(row=row_num, column=1)
    row_num += 1

    names_frame.pack(fill=X)

    ttk.Separator(frame, orient="horizontal").pack(fill="x")

    save_button = Button(frame, text="Enregistrer", command=save_config, width=20)
    save_button.pack(side=BOTTOM)
    save_button_close = Button(frame, text="Enregistrer et fermer", command=lambda: save_config(True), width=20)
    save_button_close.pack(side=BOTTOM)

    frame.pack(fill=X)

    window.mainloop()


if __name__ == "__main__":
    config_settings()
