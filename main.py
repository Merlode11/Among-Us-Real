import json
from tkinter import *
from tkinter import messagebox, ttk
from game import start_game
import os
from config_config import config_config
from player_config import player_config


def main():
    window = Tk()
    window.title("Menu principal")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("amongus.ico")

    label_title = Label(window, text="Menu principal", font=("Arial", 30))
    label_title.pack(fill=X)

    if not os.path.exists("players.json"):
        if not os.path.exists("players-exemple.json"):
            with open("players.json", "w", encoding="utf-8") as f:
                json.dump([], f)
        else:
            os.rename("players-exemple.json", "players.json")
    if not os.path.exists("config.json"):
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump({
                "impostors": 1,
                "ingeniors": 2,
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
    with open("players.json", "r", encoding="utf-8") as f:
        players = json.load(f)

    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    try:
        with open(r"/taskList/" + config["task_list"] + ".json", "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = []

    def show_config():
        clear_frame(edits_frame)
        player_label = Label(edits_frame, text=f"{len(players)} joueurs")
        player_button = Button(edits_frame, text=f"Modifier", command=player_config)
        player_label.grid(row=0, column=0)
        player_button.grid(row=0, column=1)

        task_label = Label(edits_frame, text=f"{len(tasks)} tâches")
        task_button = Button(edits_frame, text="Modifier")
        task_label.grid(row=1, column=0)
        task_button.grid(row=1, column=1)

        edits_frame.pack(fill=X)

    edits_frame = Frame(window, bg='#f5f5f5')
    show_config()

    edits_frame.pack(fill=X)

    config_button = Button(window, text="Modifier les paramètres", command=config_config)
    config_button.pack(fill=X)

    ttk.Separator(window, orient="horizontal").pack(fill="x")

    type_label = Label(window, text="Type de gestionnaire du jeu: " + config["manager_type"])
    type_label.pack(fill=X)

    play_normal_button = Button(window, text="Lancer une partie", command=lambda: begin_game(False))
    play_normal_button.pack(fill=X)

    other_plays_frame = Frame(window, bg="#f5f5f5")

    game_master_play_button = Button(other_plays_frame, text="Jouer (avec maître du jeu)")
    game_master_play_button.grid(row=0, column=0)

    without_game_master_button = Button(other_plays_frame, text="Jouer (sans maître du jeu)")
    without_game_master_button.grid(row=0, column=1)

    other_plays_frame.pack(fill=X)

    def begin_game(game_master):
        """
        Begin a game
        :param game_master: bool: If the game master is playing
        :return: None
        """
        window.destroy()
        result = start_game(game_master)
        main()

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
