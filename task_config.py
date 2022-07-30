import json
import os
from tkinter import *
from tkinter import messagebox, ttk

def task_config():
    window = Tk()
    window.title("Configurer les tâches")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("amongus.ico")
    
    choiceListFrame = Frame(window, bg="#f5f5f5")
    choiceLabel = Label(choiceListFrame, text="Sélectionnez la liste à modifier")
    choiceList = List()
