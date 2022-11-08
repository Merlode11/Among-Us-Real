import json
import os
from tkinter import *
from tkinter import messagebox, ttk
from utils import clear_frame, VerticalScrolledFrame, YesNoButton


def player_config():
    """
    Affiche la fenêtre de configuration des joueurs pour une partie en mode SMS
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
        for player in players:
            player_frame = Frame(players_frame, bg="#f5f5f5")
            player_label = Label(player_frame, text=f"{player['name']} {player['lastname']}")
            player_label.pack(side=LEFT)
            delete_button = Button(player_frame, text="Supprimer", command=lambda joueur=player: delete_player(joueur),
                                   fg="red")
            delete_button.pack(side=RIGHT)
            edit_button = Button(player_frame, text="Modifier", command=lambda joueur=player: edit_player(joueur))
            edit_button.pack(side=RIGHT)
            play_button = Button(player_frame, text="Joue" if player.get("play", True) else "Ne joue pas", command=lambda joueur=player: edit_play(joueur))
            play_button.pack(side=RIGHT)
            player_frame.pack(fill=X, anchor=N, expand=True)

        add_button = Button(players_frame, text="Ajouter un joueur", command=lambda: add_player())
        add_button.pack(side=BOTTOM)

    show_players()

    def edit_player(player: dict):
        """
        Modifie un joueur déjà créé
        """

        def save_player():
            """
            Enregistrer le joueur modifié dans le fichier JSON correspondant
            """
            new_player = {
                "name": name_entry.get(),
                "lastname": lastname_entry.get(),
                "phone": phone_entry.get(),
                "play": play_button.get_value()
            }
            players = []
            if os.path.exists("players.json"):
                with open("players.json", "r", encoding="utf-8") as file:
                    players = json.load(file)
            players[players.index(player)] = new_player
            with open("players.json", "w", encoding="utf-8") as file:
                json.dump(players, file, indent=4, ensure_ascii=False)
            edit_window.destroy()
            show_players()

        edit_window = Tk()

        def closing():
            """
            Affichage d'une fenêtre de confirmation de fermeture
            :return:
            """
            if messagebox.askokcancel("Fermer", "Voulez-vous vraiment quitter sans enregister ?", parent=edit_window):
                edit_window.destroy()

        edit_window.protocol("WM_DELETE_WINDOW", closing)
        edit_window.title(f"Modifier le joueur {player['name']} {player['lastname']}")
        edit_window.geometry("800x600")
        edit_window.resizable(True, True)
        edit_window.configure(background='#f5f5f5')
        edit_window.iconbitmap("assets/img/amongus.ico")

        names_frame = Frame(edit_window, bg="#f5f5f5")
        name_label = Label(names_frame, text="Prénom: ")
        name_entry = Entry(names_frame)
        name_entry.insert(0, player["name"])
        name_label.grid(row=0, column=0)
        name_entry.grid(row=0, column=1)

        lastname_label = Label(names_frame, text="Nom de famille: ")
        lastname_entry = Entry(names_frame)
        lastname_entry.insert(0, player["lastname"])
        lastname_label.grid(row=1, column=0)
        lastname_entry.grid(row=1, column=1)

        phone_label = Label(names_frame, text="Numéro de téléphone: ")
        phone_entry = Entry(names_frame)
        phone_entry.insert(0, player["phone"])
        phone_label.grid(row=2, column=0)
        phone_entry.grid(row=2, column=1)

        play_label = Label(names_frame, text="Le joueur joue ?")
        play_button = YesNoButton(names_frame, value=player.get("play", True))

        play_label.grid(row=3, column=0)
        play_button.grid(row=3, column=1)

        names_frame.pack(fill=X)

        save_button = Button(edit_window, text="Enregistrer", command=save_player)
        save_button.pack(side=BOTTOM)

        edit_window.mainloop()

    def delete_player(player: dict):
        """
        Supprime un joueur déjà créé
        """
        if messagebox.askokcancel("Supprimer",
                                  f"Voulez-vous vraiment supprimer le joueur {player['name']} {player['lastname']} ?",
                                  parent=window):
            players = []
            if os.path.exists("players.json"):
                with open("players.json", "r", encoding="utf-8") as file:
                    players = json.load(file)
            del players[players.index(player)]
            with open("players.json", "w", encoding="utf-8") as file:
                json.dump(players, file, indent=4, ensure_ascii=False)
            show_players()

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

        def save_player():
            """
            Sauvegarde le nouveau joueur dans le fichier JSON
            """
            if name_entry.get() == "" or lastname_entry.get() == "" or phone_entry.get() == "":
                messagebox.showerror("Erreur", "Veuillez remplir tous les champs", parent=add_window)
                return
            player = {
                "name": name_entry.get(),
                "lastname": lastname_entry.get(),
                "phone": phone_entry.get(),
                "play": play_button.get_value()
            }
            players = []
            if os.path.exists("players.json"):
                with open("players.json", "r", encoding="utf-8") as file:
                    players = json.load(file)
            players.append(player)
            with open("players.json", "w", encoding="utf-8") as file:
                json.dump(players, file, indent=4, ensure_ascii=False)
            add_window.destroy()
            show_players()

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

        names_frame = Frame(add_window, bg="#f5f5f5")
        name_label = Label(names_frame, text="Nom: ")
        name_entry = Entry(names_frame)
        name_label.grid(row=0, column=0)
        name_entry.grid(row=0, column=1)

        lastname_label = Label(names_frame, text="Nom de famille: ")
        lastname_entry = Entry(names_frame)
        lastname_label.grid(row=1, column=0)
        lastname_entry.grid(row=1, column=1)

        phone_label = Label(names_frame, text="Numéro de téléphone: ")
        phone_entry = Entry(names_frame)
        phone_label.grid(row=2, column=0)
        phone_entry.grid(row=2, column=1)

        play_label = Label(names_frame, text="Le joueur joue ?")
        play_button = YesNoButton(names_frame)

        play_label.grid(row=3, column=0)
        play_button.grid(row=3, column=1)

        names_frame.pack(fill=X)

        save_button = Button(add_window, text="Ajouter", command=save_player)
        save_button.pack(side=BOTTOM)

        add_window.mainloop()

    players_frame.pack(fill=X)
    canva_frame.pack(fill=BOTH, expand=True)

    window.mainloop()


if __name__ == "__main__":
    player_config()
