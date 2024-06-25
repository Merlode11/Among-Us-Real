import json
import os
from tkinter import *
from tkinter import messagebox, ttk
from utils import clear_frame, VerticalScrolledFrame, YesNoButton


def player_config():
    """
    Affiche la fenêtre de configuration des joueurs pour une partie en mode SMS et WhatsApp
    """
    window = Tk()
    window.title("Configurer les joueurs")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("assets/img/amongus.ico")

    canva_frame = Frame(window, bg="#f5f5f5")

    players_frame = VerticalScrolledFrame(canva_frame, width=window.winfo_width(), height=window.winfo_width())

    def show_players():
        clear_frame(players_frame)
        players = []
        if os.path.exists("players.json"):
            with open("players.json", "r", encoding="utf-8") as file:
                players = json.load(file)
        sms_frame = Frame(players_frame, bg="#f5f5f5")
        ttk.Separator(sms_frame, orient="horizontal").pack(fill="x")
        Label(sms_frame, text="SMS", font=("Arial", 25)).pack(fill=X)

        ttk.Separator(players_frame, orient="horizontal").pack(fill="x")
        insta_frame = Frame(players_frame, bg="#f5f5f5")
        Label(insta_frame, text="Instagram", font=("Arial", 25)).pack(fill=X)

        ttk.Separator(players_frame, orient="horizontal").pack(fill="x")
        discord_frame = Frame(players_frame, bg="#f5f5f5")
        Label(discord_frame, text="Discord", font=("Arial", 25)).pack(fill=X)

        ttk.Separator(players_frame, orient="horizontal").pack(fill="x")
        telegram_frame = Frame(players_frame, bg="#f5f5f5")
        Label(telegram_frame, text="Telegram", font=("Arial", 25)).pack(fill=X)

        for player in players:
            player_frame = None
            if player.get("type", "") == "sms":
                player_frame = Frame(sms_frame, bg="#f5f5f5")
            elif player.get("type", "") == "instagram":
                player_frame = Frame(insta_frame, bg="#f5f5f5")
            elif player.get("type", "") == "discord":
                player_frame = Frame(discord_frame, bg="#f5f5f5")
            elif player.get("type", "") == "telegram":
                player_frame = Frame(telegram_frame, bg="#f5f5f5")
            else:
                player_frame = Frame(players_frame, bg="#f5f5f5")
            player_label = Label(player_frame, text=get_str(player))
            player_label.pack(side=LEFT)
            delete_button = Button(player_frame, text="Supprimer", command=lambda joueur=player: delete_player(joueur),
                                   fg="red")
            delete_button.pack(side=RIGHT)
            edit_button = Button(player_frame, text="Modifier", command=lambda joueur=player: edit_player(joueur))
            edit_button.pack(side=RIGHT)
            play_button = Button(player_frame, text="Joue" if player.get("play", True) else "Ne joue pas",
                                 command=lambda joueur=player: edit_play(joueur))
            play_button.pack(side=RIGHT)
            player_frame.pack(fill=X, anchor=N, expand=True)
        sms_frame.pack(fill=X)
        insta_frame.pack(fill=X)
        discord_frame.pack(fill=X)
        telegram_frame.pack(fill=X)

        add_button = Button(players_frame, text="Ajouter un joueur", command=lambda: add_player())
        add_button.pack(side=BOTTOM)

    show_players()

    def edit_player(player: dict):
        """
        Modifie un joueur déjà créé
        """

        obj: dict = {
            "name": None,
            "phone": None,
            "username": None,
            "id": None
        }

        def save_player():
            """
            Enregistrer le joueur modifié dans le fichier JSON correspondant
            """
            if obj["name"].get() == "":
                messagebox.showerror("Erreur", "Merci de bien vouloir mettre un nom !", parent=edit_window)
                obj["name"].focus()
                return
            new_player = {
                "type": player_type.get(),
                "name": obj["name"].get(),
                "play": play_button.get_value()
            }
            if player_type.get() == "sms":
                if obj["phone"].get() == "":
                    messagebox.showerror("Erreur", "Merci de bien vouloir mettre un numéro de téléphone !",
                                         parent=edit_window)
                    obj["phone"].focus()
                    return
                new_player["phone"] = obj["phone"].get()
            elif player_type.get() == "instagram":
                if obj["username"].get() == "":
                    messagebox.showerror("Erreur", "Merci de bien vouloir mettre un nom d'utilisateur !",
                                         parent=edit_window)
                    obj["username"].focus()
                    return
                new_player["username"] = obj["username"].get()
            else:
                if obj["id"].get() == "":
                    messagebox.showerror("Erreur", "Merci de bien vouloir mettre un identifiant !", parent=edit_window)
                    obj["id"].focus()
                    return
                new_player["id"] = obj["id"].get()
            players = []
            if os.path.exists("players.json"):
                with open("players.json", "r", encoding="utf-8") as file:
                    players = json.load(file)
            players[players.index(player)] = new_player
            with open("players.json", "w", encoding="utf-8") as file:
                json.dump(players, file, indent=4, ensure_ascii=False)
            edit_window.destroy()
            window.destroy()
            return player_config()

        edit_window = Tk()

        def closing():
            """
            Affichage d'une fenêtre de confirmation de fermeture
            :return:
            """
            if messagebox.askokcancel("Fermer", "Voulez-vous vraiment quitter sans enregister ?", parent=edit_window):
                edit_window.destroy()

        edit_window.protocol("WM_DELETE_WINDOW", closing)
        edit_window.title(f"Modifier le joueur {get_str(player)}")
        edit_window.geometry("800x600")
        edit_window.resizable(True, True)
        edit_window.configure(background='#f5f5f5')
        edit_window.iconbitmap("assets/img/amongus.ico")

        type_frame = Frame(edit_window, bg="#f5f5f5")

        names_frame = Frame(edit_window, bg="#f5f5f5")

        play_label = Label(names_frame, text="Le joueur joue ?")
        play_button = YesNoButton(names_frame, value=player.get("play", True))

        def show_names(stock):
            clear_frame(names_frame)
            row_num = 0
            name_label = Label(names_frame, text="Nom: ")
            stock["name"] = name_entry = Entry(names_frame)
            name_entry.insert(0, player.get("name", ""))
            name_label.grid(row=row_num, column=0)
            name_entry.grid(row=row_num, column=1)
            row_num += 1
            if player_type.get() == "sms":
                phone_label = Label(names_frame, text="Numéro de téléphone: ")
                stock["phone"] = phone_entry = Entry(names_frame)
                phone_entry.insert(0, player.get("phone", ""))
                phone_label.grid(row=row_num, column=0)
                phone_entry.grid(row=row_num, column=1)
            elif player_type.get() == "instagram":
                username_label = Label(names_frame, text="Nom d'utilisateur: ")
                stock["username"] = username_entry = Entry(names_frame)
                username_entry.insert(0, player.get("username", ""))
                username_label.grid(row=row_num, column=0)
                username_entry.grid(row=row_num, column=1)
            elif player_type.get() == "discord":
                id_label = Label(names_frame, text="Identifiant d'utilisateur: ")
                stock["id"] = id_entry = Entry(names_frame)
                id_entry.insert(0, player.get("id", ""))
                id_label.grid(row=row_num, column=0)
                id_entry.grid(row=row_num, column=1)

            elif player_type.get() == "telegram":
                id_label = Label(names_frame, text="Identifiant d'utilisateur: ")
                stock["id"] = id_entry = Entry(names_frame)
                id_entry.insert(0, player.get("id", ""))
                id_label.grid(row=row_num, column=0)
                id_entry.grid(row=row_num, column=1)
            row_num += 1

            play_label = Label(names_frame, text="Le joueur joue ?")
            play_button = YesNoButton(names_frame, value=player.get("play", True))

            play_label.grid(row=row_num, column=0)
            play_button.grid(row=row_num, column=1)

        player_type = StringVar()
        player_type.set(player.get("type", "sms"))
        player_type_label = Label(type_frame, text="Type de joueur: ")
        player_type_entry = OptionMenu(type_frame, player_type, *["sms", "instagram", "discord", "telegram"],
                                       command=lambda x: show_names(obj))
        player_type_label.grid(row=0, column=0)
        player_type_entry.grid(row=0, column=1)

        type_frame.pack(fill=X)

        show_names(obj)

        names_frame.pack(fill=X)

        save_button = Button(edit_window, text="Enregistrer", command=save_player)
        save_button.pack(side=BOTTOM)

        edit_window.mainloop()

    def delete_player(player: dict):
        """
        Supprime un joueur déjà créé
        """
        if messagebox.askokcancel("Supprimer",
                                  f"Voulez-vous vraiment supprimer le joueur {get_str(player)} ?",
                                  parent=window):
            players = []
            if os.path.exists("players.json"):
                with open("players.json", "r", encoding="utf-8") as file:
                    players = json.load(file)
            del players[players.index(player)]
            with open("players.json", "w", encoding="utf-8") as file:
                json.dump(players, file, indent=4, ensure_ascii=False)
            window.destroy()
            return player_config()

    def edit_play(player: dict):
        """
        Modifie le statut de joueur
        """
        players = []
        if os.path.exists("players.json"):
            with open("players.json", "r", encoding="utf-8") as file:
                players = json.load(file)
        index = players.index(player)
        player["play"] = not player.get("play", True)
        players[index] = player
        with open("players.json", "w", encoding="utf-8") as file:
            json.dump(players, file, indent=4, ensure_ascii=False)
        show_players()

    def add_player():
        """
        Fenêtre pour ajouter un joueur dans la liste des joueurs
        """

        obj: dict = {
            "name": None,
            "phone": None,
            "username": None,
            "id": None
        }

        def save_player():
            """
            Enregistrer le joueur modifié dans le fichier JSON correspondant
            """
            if obj["name"].get() == "":
                messagebox.showerror("Erreur", "Merci de bien vouloir mettre un nom !", parent=add_window)
                obj["name"].focus()
                return
            new_player = {
                "type": player_type.get(),
                "name": obj["name"].get(),
                "play": play_button.get_value()
            }
            if player_type.get() == "sms":
                if obj["phone"].get() == "":
                    messagebox.showerror("Erreur", "Merci de bien vouloir mettre un numéro de téléphone !",
                                         parent=add_window)
                    obj["phone"].focus()
                    return
                new_player["phone"] = obj["phone"].get()
            elif player_type.get() == "instagram":
                if obj["username"].get() == "":
                    messagebox.showerror("Erreur", "Merci de bien vouloir mettre un nom d'utilisateur !",
                                         parent=add_window)
                    obj["username"].focus()
                    return
                new_player["username"] = obj["username"].get()
            else:
                if obj["id"].get() == "":
                    messagebox.showerror("Erreur", "Merci de bien vouloir mettre un identifiant !", parent=add_window)
                    obj["id"].focus()
                    return
                new_player["id"] = obj["id"].get()
            players = []
            if os.path.exists("players.json"):
                with open("players.json", "r", encoding="utf-8") as file:
                    players = json.load(file)
            players.append(new_player)
            with open("players.json", "w", encoding="utf-8") as file:
                json.dump(players, file, indent=4, ensure_ascii=False)
            add_window.destroy()
            window.destroy()
            return player_config()

        add_window = Tk()
        add_window.title("Ajouter un joueur")

        def closing():
            """
            Affichage d'une fenêtre de confirmation de fermeture
            :return:
            """
            if messagebox.askokcancel("Fermer", "Voulez-vous vraiment quitter sans enregister ?", parent=add_window):
                add_window.destroy()

        add_window.protocol("WM_DELETE_WINDOW", closing)

        add_window.geometry("800x600")
        add_window.resizable(True, True)
        add_window.configure(background='#f5f5f5')
        add_window.iconbitmap("assets/img/amongus.ico")

        type_frame = Frame(add_window, bg="#f5f5f5")

        names_frame = Frame(add_window, bg="#f5f5f5")

        play_label = Label(names_frame, text="Le joueur joue ?")
        play_button = YesNoButton(names_frame)

        def show_names(stock):
            clear_frame(names_frame)
            row_num = 0
            name_label = Label(names_frame, text="Nom: ")
            stock["name"] = name_entry = Entry(names_frame)
            name_label.grid(row=row_num, column=0)
            name_entry.grid(row=row_num, column=1)
            row_num += 1
            if player_type.get() == "sms":
                phone_label = Label(names_frame, text="Numéro de téléphone: ")
                stock["phone"] = phone_entry = Entry(names_frame)
                phone_label.grid(row=row_num, column=0)
                phone_entry.grid(row=row_num, column=1)
            elif player_type.get() == "instagram":
                username_label = Label(names_frame, text="Nom d'utilisateur: ")
                stock["username"] = username_entry = Entry(names_frame)
                username_label.grid(row=row_num, column=0)
                username_entry.grid(row=row_num, column=1)
            elif player_type.get() == "discord":
                username_label = Label(names_frame, text="Nom d'utilisateur: ")
                stock["username"] = username_entry = Entry(names_frame)
                username_label.grid(row=row_num, column=0)
                username_entry.grid(row=row_num, column=1)
                row_num += 1
                id_label = Label(names_frame, text="Identifiant d'utilisateur: ")
                stock["id"] = id_entry = Entry(names_frame)
                id_label.grid(row=row_num, column=0)
                id_entry.grid(row=row_num, column=1)

            elif player_type.get() == "telegram":
                id_label = Label(names_frame, text="Identifiant d'utilisateur: ")
                stock["id"] = id_entry = Entry(names_frame)
                id_label.grid(row=row_num, column=0)
                id_entry.grid(row=row_num, column=1)
            row_num += 1

            play_label = Label(names_frame, text="Le joueur joue ?")
            play_button = YesNoButton(names_frame)

            play_label.grid(row=row_num, column=0)
            play_button.grid(row=row_num, column=1)

        player_type = StringVar()
        player_type_label = Label(type_frame, text="Type de joueur: ")
        player_type_entry = OptionMenu(type_frame, player_type, *["sms", "instagram", "discord", "telegram"],
                                       command=lambda x: show_names(obj))
        player_type_label.grid(row=0, column=0)
        player_type_entry.grid(row=0, column=1)

        type_frame.pack(fill=X)

        show_names(obj)

        names_frame.pack(fill=X)

        names_frame.pack(fill=X)

        save_button = Button(add_window, text="Ajouter", command=save_player)
        save_button.pack(side=BOTTOM)

        add_window.mainloop()

    players_frame.pack(fill=X)
    canva_frame.pack(fill=BOTH, expand=True)

    window.mainloop()


def get_str(player):
    if player.get("type") == "instagram":
        return f"{player.get('name', 'Inconnu')}: {player.get('username', 'inconnu')}"
    elif player.get("type") == "sms":
        return f"{player.get('name')}: {player.get('phone', '+00000000000')}"
    elif player.get("type") == "discord":
        return f"{player.get('name', 'Inconnu')}: {player.get('id', '00000000000000000')}"
    elif player.get("type") == "telegram":
        return f"{player.get('name', 'Inconnu')}: {player.get('id', '0000000000')}"


if __name__ == "__main__":
    player_config()
