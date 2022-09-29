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

    playersFrame = Frame(window, bg="#f5f5f5")

    for player in players:
        playerFrame = Frame(playersFrame, bg="#f5f5f5")
        playerLabel = Label(playerFrame, text=f"{player['name']} {player['lastname']}")
        playerLabel.pack(side=LEFT)
        editButton = Button(playerFrame, text="Modifier", command=lambda joueur=player: edit_player(joueur))
        editButton.pack(side=RIGHT)
        playerFrame.pack(fill=X)

    playersFrame.pack(fill=X)

    addButton = Button(window, text="Ajouter un joueur", command=add_player)
    addButton.pack(side=BOTTOM)

    window.mainloop()


def edit_player(player: dict):
    def save_player():
        new_player = {
            "name": nameEntry.get(),
            "lastname": lastnameEntry.get(),
            "phone": phoneEntry.get(),
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

    namesFrame = Frame(window, bg="#f5f5f5")
    nameLabel = Label(namesFrame, text="Prénom: ")
    nameEntry = Entry(namesFrame)
    nameEntry.insert(0, player["name"])
    nameLabel.grid(row=0, column=0)
    nameEntry.grid(row=0, column=1)

    lastnameLabel = Label(namesFrame, text="Nom de famille: ")
    lastnameEntry = Entry(namesFrame)
    lastnameEntry.insert(0, player["lastname"])
    lastnameLabel.grid(row=1, column=0)
    lastnameEntry.grid(row=1, column=1)

    phoneLabel = Label(namesFrame, text="Numéro de téléphone: ")
    phoneEntry = Entry(namesFrame)
    phoneEntry.insert(0, player["phone"])
    phoneLabel.grid(row=2, column=0)
    phoneEntry.grid(row=2, column=1)

    namesFrame.pack(fill=X)

    saveButton = Button(window, text="Enregistrer", command=save_player)
    saveButton.pack(side=BOTTOM)

    window.mainloop()


def add_player():

    def save_player():
        # TODO: Save in DB
        player = {
            "name": nameEntry.get(),
            "lastname": lastnameEntry.get(),
            "phone": phoneEntry.get()
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

    namesFrame = Frame(window, bg="#f5f5f5")
    nameLabel = Label(namesFrame, text="Nom: ")
    nameEntry = Entry(namesFrame)
    nameLabel.grid(row=0, column=0)
    nameEntry.grid(row=0, column=1)

    lastnameLabel = Label(namesFrame, text="Nom de famille: ")
    lastnameEntry = Entry(namesFrame)
    lastnameLabel.grid(row=1, column=0)
    lastnameEntry.grid(row=1, column=1)

    phoneLabel = Label(namesFrame, text="Numéro de téléphone: ")
    phoneEntry = Entry(namesFrame)
    phoneLabel.grid(row=2, column=0)
    phoneEntry.grid(row=2, column=1)

    namesFrame.pack(fill=X)

    saveButton = Button(window, text="Ajouter", command=save_player)
    saveButton.pack(side=BOTTOM)

    window.mainloop()
