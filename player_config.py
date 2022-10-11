import json
import os
from tkinter import *
from tkinter import messagebox, ttk


def player_config():
    window = Tk()
    window.title("Configurer les joueurs")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("amongus.ico")

    players = []
    if os.path.exists("players.json"):
        with open("players.json", "r") as file:
            players = json.load(file)

    players_frame = Frame(window, bg="#f5f5f5")

    for player in players:
        player_frame = Frame(players_frame, bg="#f5f5f5")
        player_label = Label(player_frame, text=f"{player['name']} {player['lastname']}")
        player_label.pack(side=LEFT)
        edit_button = Button(player_frame, text="Modifier", command=lambda joueur=player: edit_player(joueur))
        edit_button.pack(side=RIGHT)
        player_frame.pack(fill=X)

    players_frame.pack(fill=X)

    add_button = Button(window, text="Ajouter un joueur", command=add_player)
    add_button.pack(side=BOTTOM)

    window.mainloop()


def edit_player(player: dict):
    def save_player():
        new_player = {
            "name": name_entry.get(),
            "lastname": lastname_entry.get(),
            "phone": phone_entry.get(),
        }
        players = []
        if os.path.exists("players.json"):
            with open("players.json", "r") as file:
                players = json.load(file)
        players[players.index(player)] = new_player
        with open("players.json", "w") as file:
            json.dump(players, file)
        window.destroy()

    window = Tk()
    window.title(f"Modifier le joueur {player['name']} {player['lastname']}")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("amongus.ico")

    names_frame = Frame(window, bg="#f5f5f5")
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

    names_frame.pack(fill=X)

    save_button = Button(window, text="Enregistrer", command=save_player)
    save_button.pack(side=BOTTOM)

    window.mainloop()


def add_player():

    def save_player():
        player = {
            "name": name_entry.get(),
            "lastname": lastname_entry.get(),
            "phone": phone_entry.get()
        }
        players = []
        if os.path.exists("players.json"):
            with open("players.json", "r") as file:
                players = json.load(file)
        players.append(player)
        with open("players.json", "w") as file:
            json.dump(players, file)

        window.destroy()

    window = Tk()
    window.title(f"Ajouter un joueur")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("amongus.ico")

    names_frame = Frame(window, bg="#f5f5f5")
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

    names_frame.pack(fill=X)

    save_button = Button(window, text="Ajouter", command=save_player)
    save_button.pack(side=BOTTOM)

    window.mainloop()
