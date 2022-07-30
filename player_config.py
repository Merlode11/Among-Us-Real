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
    
    

def edit_player(player: dict):
    window = Tk()
    window.title(f"Modifier le joueur {player["name"]} {player["lasname"]}")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("amongus.ico")
    
    namesFrame = Frame(window, bg="#f5f5f5")
    nameLabel = Label(namesFrame, text="Prénom: ")
    nameEntry = Entry(namesFrame, value=str(player["name"]))
    nameLabel.grid(0, 0)
    nameEntry.grid(0, 1)
    
    lastnameLabel = Label(namesFrame, text="Nom de famille: ")
    lastnameEntry = Entry(namesFrame, player["lastname"]))
    lastnameLabel.grid(1, 0)
    lastnameEntry.grid(1, 1)
    
    phoneLabel = Label(namesFrame, text="Numéro de téléphone: ")
    phoneEntry = Entry(namesFrame, player["phone"]))
    phoneLabel.grid(2, 0)
    phoneEntry.grid(2, 1)
    
    namesFrame.pack(fill=X)
    
    saveButton = Button(window, text="Enregistrer", command=save_player)
    saveButton.pack(side=BOTTOM)
    
    window.mainloop()
    
    def save_player(): 
        window.destroy()
        
def add_player(): 
    window = Tk()
    window.title(f"Modifier le joueur {player["name"]} {player["lasname"]}")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("amongus.ico")
    
    namesFrame = Frame(window, bg="#f5f5f5")
    nameLabel = Label(namesFrame, text="Nom: ")
    nameEntry = Entry(namesFrame)
    nameLabel.grid(0, 0)
    nameEntry.grid(0, 1)
    
    lastnameLabel = Label(namesFrame, text="Nom de famille: ")
    lastnameEntry = Entry(namesFrame))
    lastnameLabel.grid(1, 0)
    lastnameEntry.grid(1, 1)
    
    phoneLabel = Label(namesFrame, text="Numéro de téléphone: ")
    phoneEntry = Entry(namesFrame))
    phoneLabel.grid(2, 0)
    phoneEntry.grid(2, 1)
    
    namesFrame.pack(fill=X)
    
    saveButton = Button(window, text="Ajouter", command=save_player)
    saveButton.pack(side=BOTTOM)
    
    def save_player(): 
        # TODO: Save in DB
        
        nameEntry.config(value="")
        lastnameEntry.config(value="")
        phoneEntry.config(value="")
        
    
    window.mainloop()
