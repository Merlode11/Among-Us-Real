import json
from tkinter import *
from tkinter import messagebox, ttk
from game import start_game
from os.path import exists


def main():
    window = Tk()
    window.title("Menu principal")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("amongus.ico")

    label_title = Label(window, text="Menu principal", font=("Arial", 30))
    label_title.pack(fill=X)

    if not exists("players.json"):
        with open("players.json", "w") as f:
            json.dump([], f)
    if not exists("config.json"):
        with open("config.json", "w") as f:
            json.dump({
                "impostors": 1,
                "ingenors": 2,
                "scientists": 1,
                "tasks": 3,
                "max_task_given": 2,
                "ip": "172.20.10.10",
                "names": {
                    "impostor": "Imposteur",
                    "scientist": "Scientifique",
                    "ingenior": "Ingenieur",
                    "crewmate": "Membre de l'équipe",
                    "title": "Among Us Réel"
                },
                "max_dead_check": 4,
                "game_master": False,
                "show_dead_roles": False,
                "discussion_time": 120,
                "vote_time": 30,
                "task_list": "task-exemple",
                "manager_type": "sms",
                "min_before_inactiv_warn": 5,
                "max_warns": 3
            }, f)
    with open("players.json", "r", encoding='utf-8') as f:
        players = json.load(f)

    with open("config.json", "r", encoding='utf-8') as f:
        config = json.load(f)

    try:
        with open(r"/taskList/" + config["task_list"] + ".json", "r", encoding='utf-8') as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = []

    def show_config():
        clear_frame(editsFrame)
        playerLabel = Label(editsFrame, text=f"{len(players)} joueurs")
        playerButton = Button(editsFrame, text=f"Modifier")
        playerLabel.grid(row=0, column=0)
        playerButton.grid(row=0, column=1)

        taskLabel = Label(editsFrame, text=f"{len(tasks)} tâches")
        taskButton = Button(editsFrame, text="Modifier")
        taskLabel.grid(row=1, column=0)
        taskButton.grid(row=1, column=1)

        editsFrame.pack(fill=X)

    editsFrame = Frame(window, bg='#f5f5f5')
    show_config()

    editsFrame.pack(fill=X)

    configButton = Button(window, text="Modifier les paramètres")
    configButton.pack(fill=X)

    ttk.Separator(window, orient="horizontal").pack(fill="x")

    typeLabel = Label(window, text="Type de gestionnaire du jeu: " + config["manager_type"])
    typeLabel.pack(fill=X)

    playNormalButton = Button(window, text="Lancer une partie", command=lambda: begin_game(False))
    playNormalButton.pack(fill=X)

    otherPlaysFrame = Frame(window, bg="#f5f5f5")

    gameMasterPlayButton = Button(otherPlaysFrame, text="Jouer (avec maître du jeu)")
    gameMasterPlayButton.grid(row=0, column=0)

    withoutGameMasterButton = Button(otherPlaysFrame, text="Jouer (sans maître du jeu)")
    withoutGameMasterButton.grid(row=0, column=1)

    otherPlaysFrame.pack(fill=X)

    def begin_game(game_master):
        """
        Begin a game
        :param game_master: bool: If the game master is playing
        :return: None
        """
        window.destroy()
        start_game(game_master)

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
