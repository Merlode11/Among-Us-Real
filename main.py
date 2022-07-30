import json
from tkinter import *
from tkinter import messagebox, ttk

def main():
    window = Tk()
    window.title("Menu principal")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("amongus.ico")

    label_title = Label(window, text="Menu principal", font=("Arial", 30))
    label_title.pack(fill=X)
    
    with open("players.json", "r", encoding='utf-8') as f:
        players = json.load(f)
    
    with open(r"/taskList/" + self.config["task_list"] + ".json", "r", encoding='utf-8') as f:
    
    with open("config.json", "r", encoding='utf-8') as f:
        config = json.load(f)
    
    editsFrame = Frame(window, bg='#f5f5f5')
    show_config()
    
    editsFrame.pack(fill=X)
    
    configButton = Button(window, text="Modifier les paramètres")
    configButton.pack(fill=X)
    
    ttk.Separator(window, orient="horizontal").pack(fill="x")
    
    typeLabel = Label(window, text="Type de gestionnaire du jeu: " + config["manager_type"])
    typeLabel.pack(fill=X)
    
    playNormalButton = Button(window, text="Lancer une partie")
    playNormalButton.pack(fill=X)
    
    otherPlaysFrame = Frame(window, bg="#f5f5f5")
    
    gameMasterPlayButton = Button(otherPlaysFrame, text="Jouer (avec maître du jeu)")
    gameMasterPlayButton.grid(0, 0)
    
    withoutGameMasterButton = Button(otherPlaysFrame, text="Jouer (sans maître du jeu)")
    withoutGameMasterButton.grid(0, 1)
    
    otherPlaysFrame.pack(fill=X)
    
    def show_config(): 
        clear_frame(editsFrame)
        playerLabel = Label(editsFrame, text=f"{len(players)} joueurs")
        playerButton = Button(editsFrame, text=f"Modifier")
        playerLabel.grid(0, 0)
        playerButton.grid(0, 1)
            
        taskLabel = Label(editsFrame, text=f"{len(tasks)} tâches")
        taskButton = Button(editsFrame, text="Modifier")
        taskLabel.grid(1, 0)
        taskButton.grid(1, 1)
            
        editsFrame.pack(fill=X)
    
    def begin_game(game_master):
        
    window.mainloop()

def clear_frame(frame: Frame):
    """
    Clear all entries in a frame
    :param frame: Frame: Frame to clear
    :return: None
    """
    for widget in frame.winfo_children():
        if widget.winfo_class() == "Frame":
            clear_frame(widget)
        widget.destroy()


if __name__ == "__main__": 
    main()
