import json
from tkinter import *
from tkinter import messagebox, ttk
from sms.sms_game_class import SMSGame
from web.web_game_class import WebGame
import os
from config_settings import config_settings
from player_config import player_config
from task_config import task_config
from utils import clear_frame


def main():
    """
    Affichage de la fenêtre d'accueil
    """
    window = Tk()
    window.title("Among Us Real - Menu principal")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("assets/img/amongus.ico")

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
                "engineers": 2,
                "scientists": 1,
                "tasks": 3,
                "max_task_given": 2,
                "ip": "172.20.10.10",
                "names": {
                    "impostor": "Imposteur",
                    "scientist": "Scientifique",
                    "engineer": "Ingénieur",
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
        players: list = json.load(f)

    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    try:
        with open(r"/taskList/" + config["task_list"] + ".json", "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = []

    def config_players():
        global players
        player_config()
        with open("players.json", "r", encoding="utf-8") as p:
            players = json.load(p)
        show_config()

    def config_tasks():
        global tasks
        task_config()
        with open(f"taskList/{config['task_list']}.json", "r", encoding="utf-8") as t:
            tasks = json.load(t)
        show_config()

    def show_config():
        """
        Affiche dans la fenêtre la configuration actuelle de la partie
        """
        play_players = [player for player in players if player.get("play")]
        clear_frame(edits_frame)
        player_label = Label(edits_frame, text=f"Joueurs ({len(play_players)}/{len(players)})")
        player_button = Button(edits_frame, text=f"Modifier", command=config_players)
        player_label.grid(row=0, column=0)
        player_button.grid(row=0, column=1)

        task_label = Label(edits_frame, text=f"{len(tasks)} tâches")
        task_button = Button(edits_frame, text="Modifier", command=config_tasks)
        task_label.grid(row=1, column=0)
        task_button.grid(row=1, column=1)

        edits_frame.pack(fill=X)

    edits_frame = Frame(window, bg='#f5f5f5')
    show_config()

    edits_frame.pack(fill=X)

    config_button = Button(window, text="Modifier les paramètres", command=config_settings)
    config_button.pack(fill=X)

    ttk.Separator(window, orient="horizontal").pack(fill="x")

    type_label = Label(window, text="Type de gestionnaire du jeu: " + config["manager_type"])
    type_label.pack(fill=X)

    play_normal_button = Button(window, text="Lancer une partie", command=lambda: begin_game())
    play_normal_button.pack(fill=X)

    other_plays_frame = Frame(window, bg="#f5f5f5")

    game_master_play_button = Button(other_plays_frame, text="Jouer (avec maître du jeu)",
                                     command=lambda: begin_game(True))
    game_master_play_button.grid(row=0, column=0)

    without_game_master_button = Button(other_plays_frame, text="Jouer (sans maître du jeu)",
                                        command=lambda: begin_game(False))
    without_game_master_button.grid(row=0, column=1)

    other_plays_frame.pack(fill=X)

    def begin_game(game_master: bool or None = None):
        """
        Commencer une partie
        :param game_master: bool: If the game master is playing
        :return: None
        """
        window.destroy()
        if config["manager_type"] == "sms":
            SMSGame(game_master)
        elif config["manager_type"] == "web":
            WebGame(game_master)
        else:
            messagebox.showerror("Erreur", "Le gestionnaire de jeu n'est pas reconnu")
        main()

    window.mainloop()


if __name__ == "__main__":
    main()
