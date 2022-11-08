import json
import os
from tkinter import *
from tkinter import messagebox
from utils import clear_frame


def task_config():
    """
    Affiche la fenêtre de configuration des tâches
    :return:
    """

    def manage_names():
        manage_list_names()
        print("manage names")

    window = Tk()
    window.title("Configurer les tâches")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("assets/img/amongus.ico")

    choiceListFrame = Frame(window, bg="#f5f5f5")
    choiceLabel = Label(choiceListFrame, text="Sélectionnez la liste à modifier")

    with open("config.json", "r", encoding='utf8') as file:
        config = json.load(file)

    tasks = [liste.replace(".json", "") for liste in os.listdir("taskList") if liste.endswith(".json")]
    if len(tasks) == 0:
        create_task_list()

    if config["tasks"] not in tasks:
        config["tasks"] = tasks[0]

    choice = StringVar()
    choice.set(config["task_list"])
    choiceList = OptionMenu(choiceListFrame, choice, *tasks)
    choiceLabel.grid(row=0, column=0)
    choiceList.grid(row=0, column=1)

    manageButton = Button(choiceListFrame, text="Gérer", command=manage_names)
    manageButton.grid(row=0, column=2)

    choiceListFrame.pack(fill=X, anchor=N)

    editTaskFrame = Frame(window, bg="#f5f5f5")

    def refresh_tasks():
        clear_frame(editTaskFrame)
        with open(f"taskList/{config['task_list']}.json", "r", encoding="utf-8") as file:
            tasks: list = json.load(file)
        for i in range(len(tasks)):
            task = tasks[i]
            taskFrame = Frame(editTaskFrame, bg="#f5f5f5")
            taskLabel = Label(taskFrame, text=task["name"])
            editButton = Button(taskFrame, text="Modifier", command=lambda t=task: edit_task(t))
            deleteButton = Button(taskFrame, text="Supprimer", command=lambda t=task: delete_task(t))
            taskLabel.grid(row=i, column=0)
            editButton.grid(row=i, column=1)
            deleteButton.grid(row=i, column=2)
            taskFrame.pack(fill=X)

    refresh_tasks()
    editTaskFrame.pack(fill=X)

    window.mainloop()


def create_task_list() -> None:
    """
    Affiche une fenêtre pour créer une nouvelle liste de tâches
    :return:
    """
    window = Tk()
    window.title("Créer une liste de tâches")
    window.geometry("400x100")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("assets/img/amongus.ico")

    nameFrame = Frame(window, bg="#f5f5f5")
    nameLabel = Label(nameFrame, text="Nom de la liste: ")
    nameEntry = Entry(nameFrame)
    nameLabel.grid(row=0, column=0)
    nameEntry.grid(row=0, column=1)

    nameFrame.pack(fill=X)

    def save_list() -> str or None:
        """
        Enregistrer la liste et fermer ma fenêtre 
        """
        name = nameEntry.get()
        if name == "":
            messagebox.showerror("Erreur", "Le nom de la liste ne peut pas être vide", parent=window)
            return
        if name in [liste.replace(".json", "") for liste in os.listdir("taskList") if liste.endswith(".json")]:
            messagebox.showerror("Erreur", "Une liste de tâches avec ce nom existe déjà", parent=window)
            return
        with open(f"taskList/{name}.json", "w", encoding="utf-8") as file:
            json.dump([], file, indent=4, ensure_ascii=False)
        window.destroy()
        return name

    saveButton = Button(window, text="Enregistrer", command=save_list)
    saveButton.pack(side=BOTTOM)

    window.mainloop()
    return None


def manage_list_names():
    """
    Gérer les listes, modifier le nom, en créer, supprimer
    """
    window = Tk()
    window.title("Gérer les noms de liste")
    window.geometry("400x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("assets/img/amongus.ico")

    nameFrame = Frame(window, bg="#f5f5f5")
    titre = Label(nameFrame, text="Listes de tâches disponibles")
    titre.pack(fill=X, anchor=N)

    listFrame = Frame(window, bg="#f5f5f5")

    def refresh_list() -> None:
        """
        Affiche la liste des listes de tâches disponibles
        :return:
        """

        def change_list(name: str) -> None:
            """
            Change la liste de tâches effective pour le jeu
            :param name: str: Le nom de la tâche
            :return:
            """
            config["task_list"] = name
            with open("config.json", "w", encoding='utf8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
            refresh_list()

        def edit_list_name(name: str) -> None:
            """
            Permet de modifier le nom d'une liste de tâches
            :param name: str: Le nom de la tâche à modifier
            :return:
            """
            edit_window = Tk()
            edit_window.title("Modifier le nom de la liste")
            edit_window.geometry("400x100")
            edit_window.resizable(True, True)
            edit_window.configure(background='#f5f5f5')
            edit_window.iconbitmap("assets/img/amongus.ico")

            name_frame = Frame(edit_window, bg="#f5f5f5")
            nameLabel = Label(name_frame, text="Nom de la liste: ")
            nameEntry = Entry(name_frame)
            nameEntry.insert(0, name)
            nameLabel.grid(row=0, column=0)
            nameEntry.grid(row=0, column=1)

            name_frame.pack(fill=X)

            def save_list() -> None:
                """
                Enregistre le nouveau nom de la liste
                :return:
                """
                new_name = nameEntry.get()
                if new_name == "":
                    messagebox.showerror("Erreur", "Le nom de la liste ne peut pas être vide", parent=edit_window)
                    return
                if new_name in [liste.replace(".json", "") for liste in os.listdir("taskList") if
                                liste.endswith(".json")]:
                    messagebox.showerror("Erreur", "Une liste de tâches avec ce nom existe déjà", parent=edit_window)
                    return
                os.rename(f"taskList/{name}.json", f"taskList/{new_name}.json")
                if config["task_list"] == name:
                    config["task_list"] = new_name
                    with open("config.json", "w", encoding='utf8') as f:
                        json.dump(config, f, indent=4, ensure_ascii=False)
                edit_window.destroy()
                refresh_list()

            saveButton = Button(edit_window, text="Enregistrer", command=save_list)
            saveButton.pack(side=BOTTOM)

            edit_window.mainloop()

        def del_list(name: str) -> None:
            """
            Supprime une liste de tâches
            :param name: str: Le nom de la tâche à supprimer
            :return:
            """
            if messagebox.askyesno("Supprimer la liste", "Voulez-vous vraiment supprimer cette liste ?", parent=window):
                os.remove(f"taskList/{name}.json")
                refresh_list()

        clear_frame(listFrame)
        with open("config.json", "r", encoding='utf8') as file:
            config = json.load(file)

        tasks = [liste.replace(".json", "") for liste in os.listdir("taskList") if liste.endswith(".json")]

        for i in range(len(tasks)):
            task = tasks[i]
            label = Label(listFrame, text=task)
            label.grid(row=i + 1, column=0)
            if task == config["task_list"]:
                label.config(fg="green")
            else:
                label.config(fg="red")

            choose = Button(listFrame, text="Choisir", command=lambda task_name=task: change_list(f"{task_name}"),
                            state=DISABLED if task == config["task_list"] else NORMAL)
            choose.grid(row=i + 1, column=1)
            edit = Button(listFrame, text="Modifier", command=lambda task_name=task: edit_list_name(f"{task_name}"))
            edit.grid(row=i + 1, column=2)
            delete = Button(listFrame, text="Supprimer", command=lambda task_name=task: del_list(f"{task_name}"))
            delete.grid(row=i + 1, column=3)
        window.update()

    def create_list():
        """
        Créer une nouvelle liste de tâches
        :return:
        """
        print(create_task_list())
        refresh_list()

    createButton = Button(nameFrame, text="Créer une liste", command=create_list)
    createButton.pack(fill=X, anchor=N)
    nameFrame.pack(fill=X, anchor=N)

    nameFrame.pack(fill=X)

    refresh_list()
    listFrame.pack(fill=X)

    window.mainloop()


if __name__ == "__main__":
    task_config()
