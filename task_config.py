import json
import os
from tkinter import *
from tkinter import messagebox
from utils import clear_frame, TagsEntry, VerticalScrolledFrame, IntEntry
import re

task_type_name = {
    "basic": "Basique",
    "validate_basic": "Avec Validation",
    "activate_basic": "Avec Activation",
    "activ_valid": "Avec Activation et Validation",
    "Basique": "basic",
    "Avec Validation": "validate_basic",
    "Avec Activation": "activate_basic",
    "Avec Activation et Validation": "activ_valid"
}


def task_config():
    """
    Affiche la fenêtre de configuration des tâches
    :return:
    """

    def manage_names():
        manage_list_names()

    window = Tk()
    window.title("Configurer les tâches")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("assets/img/amongus.ico")

    choice_list_frame = Frame(window, bg="#f5f5f5")
    choice_label = Label(choice_list_frame, text="Sélectionnez la liste à modifier", font=("Arial", 14))

    with open("config.json", "r", encoding='utf8') as file:
        config = json.load(file)

    tasks = [liste.replace(".json", "") for liste in os.listdir("taskList") if liste.endswith(".json")]
    if len(tasks) == 0:
        create_task_list()

    if config["task_list"] not in tasks:
        config["task_list"] = tasks[0]

    choice = StringVar()
    choice.set(config["task_list"])
    choice_list = OptionMenu(choice_list_frame, choice, *tasks)
    choice_label.grid(row=0, column=0)
    choice_list.grid(row=0, column=1)

    manage_button = Button(choice_list_frame, text="Gérer les listes", font=("Arial", 14), command=manage_names)
    manage_button.grid(row=0, column=2)

    choice_list_frame.pack(fill=X, anchor=N)

    edit_task_frame = VerticalScrolledFrame(window, bg="#f5f5f5")

    with open(f"taskList/{config['task_list']}.json", "r", encoding="utf-8") as file:
        tasks_list: list = json.load(file)

    def edit_task(task: dict):
        """
        Affiche la fenêtre pour éditer une tâche
        :param task: La tâche à éditer
        :return:
        """
        edit_window = Tk()
        edit_window.title("Éditer une tâche")
        edit_window.geometry("800x600")
        edit_window.resizable(True, True)
        edit_window.configure(background='#f5f5f5')
        edit_window.iconbitmap("assets/img/amongus.ico")

        edit_frame = VerticalScrolledFrame(edit_window, bg="#f5f5f5")

        tags_frame = Frame(edit_frame, bg="#f5f5f5")

        obj: dict[str: TagsEntry or Text or None] = {
            "keywords": None,
            "activation": None,
            "message": None
        }

        def show_tags(stock):
            clear_frame(tags_frame)

            stock["keywords"] = keywords = TagsEntry(tags_frame, tags=task.get("keywords", []))
            stock["activation"] = activation = TagsEntry(tags_frame, tags=task.get("activ_keywords", []))
            stock["message"] = message = Text(tags_frame, height=5, width=50)

            if type_choice.get() == "Avec Validation":
                keywords_label = Label(tags_frame, text="Mots-clés de validation: ")
                keywords_label.grid(row=1, column=0)
                keywords.grid(row=1, column=1)
            elif type_choice.get() == "Avec Activation":
                activation_label = Label(tags_frame, text="Mots-clé d'activation: ")
                activation_label.grid(row=1, column=0)

                message_label = Label(tags_frame, text="Message d'activation: ")
                message.insert(INSERT, task.get("message", ""))
                message_label.grid(row=2, column=0)
                message.grid(row=2, column=1)
                activation.grid(row=1, column=1)
            elif type_choice.get() == "Avec Activation et Validation":
                keywords_label = Label(tags_frame, text="Mots-clés de validation: ")
                keywords_label.grid(row=1, column=0)
                keywords.grid(row=1, column=1)
                activation.grid(row=2, column=1)

                activation_label = Label(tags_frame, text="Mots-clé d'activation: ")
                activation_label.grid(row=2, column=0)

                message_label = Label(tags_frame, text="Message d'activation: ")
                message.insert(INSERT, task.get("message", ""))
                message_label.grid(row=3, column=0)
                message.grid(row=3, column=1)


        type_frame = Frame(edit_frame, bg="#f5f5f5")
        type_label = Label(type_frame, text="Type de tâche: ")
        type_choice = StringVar()
        type_choice.set(task_type_name[task["type"]])

        type_list = OptionMenu(type_frame, type_choice, *["Basique", "Avec Validation", "Avec Activation",
                                                          "Avec Activation et Validation"],
                               command=lambda x: show_tags(obj))

        type_label.grid(row=0, column=0)
        type_list.grid(row=0, column=1)
        type_frame.pack(fill=X)

        name_frame = Frame(edit_frame, bg="#f5f5f5")
        name_label = Label(name_frame, text="Nom de la tâche: ")
        name_entry = Entry(name_frame)
        name_entry.insert(0, task["name"])
        name_label.grid(row=0, column=0)
        name_entry.grid(row=0, column=1)
        name_frame.pack(fill=X)

        description_frame = Frame(edit_frame, bg="#f5f5f5")
        description_label = Label(description_frame, text="Description de la tâche: ")
        description_text = Text(description_frame, height=5, width=50)
        description_text.insert(INSERT, task["description"])
        description_label.grid(row=1, column=0)
        description_text.grid(row=1, column=1)
        description_frame.pack(fill=X)

        location_frame = Frame(edit_frame, bg="#f5f5f5")
        location_label = Label(location_frame, text="Emplacement de la tâche: ")
        location_entry = Entry(location_frame)
        location_entry.insert(0, task["location"])
        location_label.grid(row=2, column=0)
        location_entry.grid(row=2, column=1)
        location_frame.pack(fill=X)

        steps_frame = Frame(edit_frame, bg="#f5f5f5")
        steps_label = Label(steps_frame, text="Nombre d'étapes de la tâche: ")
        steps_entry = IntEntry(steps_frame, value=task["steps"] if "steps" in task else 1)
        steps_label.grid(row=3, column=0)
        steps_entry.grid(row=3, column=1)
        steps_frame.pack(fill=X)

        show_tags(obj)
        tags_frame.pack(fill=X)

        def save_task() -> str or None:
            """
            Enregistrer la tâche et fermer ma fenêtre
            """
            task_index = tasks_list.index(task)
            name = name_entry.get()
            if name == "":
                messagebox.showerror("Erreur", "Le nom de la tâche ne peut pas être vide", parent=edit_window)
                return
            if name in [tache["name"] for tache in tasks_list if tache["name"] != task["name"]]:
                messagebox.showerror("Erreur", "Une tâche avec ce nom existe déjà", parent=edit_window)
                return
            task["name"] = name
            task["description"] =  re.sub(r"\n+$", "", description_text.get("1.0", END))
            task["location"] = location_entry.get()
            task["steps"] = steps_entry.get_value()
            task["type"] = task_type_name[type_choice.get()]

            if type_choice.get() == "Avec Validation":
                task["keywords"] = obj["keywords"].get_tags()
            elif type_choice.get() == "Avec Activation":
                task["activ_keywords"] = obj["activation"].get_tags()
                task["message"] = re.sub(r"\n+$", "", obj["message"].get("1.0", END))
            elif type_choice.get() == "Avec Activation et Validation":
                task["keywords"] = obj["keywords"].get_tags()
                task["activ_keywords"] = obj["activation"].get_tags()
                task["message"] = re.sub(r"\n+$", "", obj["message"].get("1.0", END))

            tasks_list[task_index] = task

            with open(f"taskList/{config['task_list']}.json", "w", encoding="utf-8") as file:
                json.dump(tasks_list, file, indent=4, ensure_ascii=False)

            edit_window.destroy()
            return name

        save_button = Button(edit_frame, text="Enregistrer", command=save_task)
        save_button.pack(side=BOTTOM)
        edit_frame.pack(fill=X)

        edit_window.mainloop()

    def add_task():
        """
        Ajouter une tâche
        """
        add_window = Tk()
        add_window.title("Éditer une tâche")
        add_window.geometry("800x600")
        add_window.resizable(True, True)
        add_window.configure(background='#f5f5f5')
        add_window.iconbitmap("assets/img/amongus.ico")

        add_frame = VerticalScrolledFrame(add_window, bg="#f5f5f5")

        tags_frame = Frame(add_frame, bg="#f5f5f5")

        obj: dict[str, TagsEntry or Text or None] = {
            "keywords": None,
            "activation": None,
            "message": None
        }

        def show_tags(stock: dict[str, TagsEntry or Text or None]):
            clear_frame(tags_frame)

            stock["keywords"] = keywords = TagsEntry(tags_frame)
            stock["activation"] = activation = TagsEntry(tags_frame)
            stock["message"] = message = Text(tags_frame, height=5, width=50)

            if type_choice.get() == "Avec Validation":
                keywords_label = Label(tags_frame, text="Mots-clés de validation: ")
                keywords_label.grid(row=1, column=0)
                keywords.grid(row=1, column=1)
            elif type_choice.get() == "Avec Activation":
                activation_label = Label(tags_frame, text="Mots-clé d'activation: ")
                activation_label.grid(row=1, column=0)
                activation.grid(row=1, column=1)

                message_label = Label(tags_frame, text="Message d'activation: ")
                message_label.grid(row=2, column=0)
                message.grid(row=2, column=1)
            elif type_choice.get() == "Avec Activation et Validation":
                keywords_label = Label(tags_frame, text="Mots-clés de validation: ")
                keywords = TagsEntry(tags_frame)
                keywords_label.grid(row=1, column=0)
                keywords.grid(row=1, column=1)

                activation_label = Label(tags_frame, text="Mots-clé d'activation: ")
                activation = TagsEntry(tags_frame)
                activation_label.grid(row=2, column=0)
                activation.grid(row=2, column=1)

                message_label = Label(tags_frame, text="Message d'activation: ")
                message_label.grid(row=3, column=0)
                message.grid(row=3, column=1)

        type_frame = Frame(add_frame, bg="#f5f5f5")
        type_label = Label(type_frame, text="Type de tâche: ")
        type_choice = StringVar()
        type_choice.set("Basique")

        type_list = OptionMenu(type_frame, type_choice, *["Basique", "Avec Validation", "Avec Activation",
                                                          "Avec Activation et Validation"],
                               command=lambda x: show_tags(obj))

        type_label.grid(row=0, column=0)
        type_list.grid(row=0, column=1)
        type_frame.pack(fill=X)

        name_frame = Frame(add_frame, bg="#f5f5f5")
        name_label = Label(name_frame, text="Nom de la tâche: ")
        name_entry = Entry(name_frame)
        name_label.grid(row=0, column=0)
        name_entry.grid(row=0, column=1)
        name_frame.pack(fill=X)

        description_frame = Frame(add_frame, bg="#f5f5f5")
        description_label = Label(description_frame, text="Description de la tâche: ")
        description_text = Text(description_frame, height=5, width=50)
        description_label.grid(row=1, column=0)
        description_text.grid(row=1, column=1)
        description_frame.pack(fill=X)

        location_frame = Frame(add_frame, bg="#f5f5f5")
        location_label = Label(location_frame, text="Emplacement de la tâche: ")
        location_entry = Entry(location_frame)
        location_label.grid(row=2, column=0)
        location_entry.grid(row=2, column=1)
        location_frame.pack(fill=X)

        steps_frame = Frame(add_frame, bg="#f5f5f5")
        steps_label = Label(steps_frame, text="Nombre d'étapes de la tâche: ")
        steps_entry = IntEntry(steps_frame, value=1)
        steps_label.grid(row=3, column=0)
        steps_entry.grid(row=3, column=1)
        steps_frame.pack(fill=X)

        show_tags(obj)
        tags_frame.pack(fill=X)

        def save_task() -> str or None:
            """
            Enregistrer la tâche et fermer ma fenêtre
            """
            name = name_entry.get()
            if name == "":
                messagebox.showerror("Erreur", "Le nom de la tâche ne peut pas être vide", parent=add_window)
                return
            if name in [tache["name"] for tache in tasks_list]:
                messagebox.showerror("Erreur", "Une tâche avec ce nom existe déjà", parent=add_window)
                return
            location = location_entry.get()
            if location == "":
                messagebox.showerror("Erreur", "L'emplacement de la tâche ne peut pas être vide", parent=add_window)
                return
            task = {"name": name, "description": re.sub(r"\n+$", "", description_text.get("1.0", END), flags=re.G), "location": location,
                    "steps": steps_entry.get_value(), "type": task_type_name[type_choice.get()]}
            if type_choice.get() == "Avec Validation":
                if obj["keywords"] and obj["keywords"].get_tags() == []:
                    messagebox.showerror("Erreur", "Il faut au moins un mot-clé de validation", parent=add_window)
                    return
                task["keywords"] = obj["keywords"].get_tags()
            elif type_choice.get() == "Avec Activation":
                if obj["activation"] and obj["activation"].get_tags() == []:
                    messagebox.showerror("Erreur", "Il faut au moins un mot-clé d'activation", parent=add_window)
                    return
                if obj["message"] and obj["message"].get("1.0", END) == "":
                    messagebox.showerror("Erreur", "Le message d'activation ne peut pas être vide", parent=add_window)
                    return
                task["activ_keywords"] = obj["activation"].get_tags()
                task["message"] = re.sub(r"\n+$", "", obj["message"].get("1.0", END))
            elif type_choice.get() == "Avec Activation et Validation":
                if obj["keywords"] and obj["keywords"].get_tags() == []:
                    messagebox.showerror("Erreur", "Il faut au moins un mot-clé de validation", parent=add_window)
                    return
                if obj["activation"] and obj["activation"].get_tags() == []:
                    messagebox.showerror("Erreur", "Il faut au moins un mot-clé d'activation", parent=add_window)
                    return
                if obj["message"] and obj["message"].get("1.0", END) == "":
                    messagebox.showerror("Erreur", "Le message d'activation ne peut pas être vide", parent=add_window)
                    return
                task["keywords"] = obj["keywords"].get_tags()
                task["activ_keywords"] = obj["activation"].get_tags()
                task["message"] = re.sub(r"\n+$", "", obj["message"].get("1.0", END))

            tasks_list.append(task)

            with open(f"taskList/{config['task_list']}.json", "w", encoding="utf-8") as file:
                json.dump(tasks_list, file, indent=4, ensure_ascii=False)

            add_window.destroy()
            return name

        save_button = Button(add_frame, text="Enregistrer", command=save_task)
        save_button.pack(side=BOTTOM)
        add_frame.pack(fill=X)

        add_window.mainloop()

    def delete_task(task: dict):
        """
        Supprimer une tâche
        """
        with open(f"taskList/{config['task_list']}.json", "r", encoding="utf-8") as file:
            tasks_list: list = json.load(file)
        tasks_list.remove(task)
        with open(f"taskList/{config['task_list']}.json", "w", encoding="utf-8") as file:
            json.dump(tasks_list, file, indent=4, ensure_ascii=False)
        messagebox.showinfo("Succès", "La tâche a été supprimée avec succès", parent=window)
        refresh_tasks()

    def refresh_tasks():
        clear_frame(edit_task_frame)
        with open(f"taskList/{config['task_list']}.json", "r", encoding="utf-8") as file:
            tasks_list: list = json.load(file)
        for i in range(len(tasks_list)):
            task = tasks_list[i]
            task_frame = Frame(edit_task_frame, bg="#f5f5f5")
            task_label = Label(task_frame, text=task["name"])
            edit_button = Button(task_frame, text="Modifier", command=lambda t=task: edit_task(t))
            delete_button = Button(task_frame, text="Supprimer", command=lambda t=task: delete_task(t))
            task_label.grid(row=i, column=0)
            edit_button.grid(row=i, column=1)
            delete_button.grid(row=i, column=2)
            task_frame.pack(fill=X)

        add_task_frame = Frame(edit_task_frame, bg="#f5f5f5")
        add_task_button = Button(add_task_frame, text="Ajouter une tâche", command=add_task)
        add_task_button.pack(side=BOTTOM)
        add_task_frame.pack(fill=X)
        edit_task_frame.pack(fill=X)

    refresh_tasks()
    edit_task_frame.pack(fill=X)

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

    name_frame = Frame(window, bg="#f5f5f5")
    name_label = Label(name_frame, text="Nom de la liste: ")
    name_entry = Entry(name_frame)
    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)

    name_frame.pack(fill=X)

    def save_list() -> str or None:
        """
        Enregistrer la liste et fermer ma fenêtre 
        """
        name = name_entry.get()
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

    save_button = Button(window, text="Enregistrer", command=save_list)
    save_button.pack(side=BOTTOM)

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

    name_frame = Frame(window, bg="#f5f5f5")
    titre = Label(name_frame, text="Listes de tâches disponibles")
    titre.pack(fill=X, anchor=N)

    list_frame = Frame(window, bg="#f5f5f5")

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

            edit_name_frame = Frame(edit_window, bg="#f5f5f5")
            name_label = Label(edit_name_frame, text="Nom de la liste: ")
            name_entry = Entry(edit_name_frame)
            name_entry.insert(0, name)
            name_label.grid(row=0, column=0)
            name_entry.grid(row=0, column=1)

            edit_name_frame.pack(fill=X)

            def save_list() -> None:
                """
                Enregistre le nouveau nom de la liste
                :return:
                """
                new_name = name_entry.get()
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

            save_button = Button(edit_window, text="Enregistrer", command=save_list)
            save_button.pack(side=BOTTOM)

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

        clear_frame(list_frame)
        with open("config.json", "r", encoding='utf8') as file:
            config = json.load(file)

        tasks = [liste.replace(".json", "") for liste in os.listdir("taskList") if liste.endswith(".json")]

        for i in range(len(tasks)):
            task = tasks[i]
            label = Label(list_frame, text=task)
            label.grid(row=i + 1, column=0)
            if task == config["task_list"]:
                label.config(fg="green")
            else:
                label.config(fg="red")

            choose = Button(list_frame, text="Choisir", command=lambda task_name=task: change_list(f"{task_name}"),
                            state=DISABLED if task == config["task_list"] else NORMAL)
            choose.grid(row=i + 1, column=1)
            edit = Button(list_frame, text="Modifier", command=lambda task_name=task: edit_list_name(f"{task_name}"))
            edit.grid(row=i + 1, column=2)
            delete = Button(list_frame, text="Supprimer", command=lambda task_name=task: del_list(f"{task_name}"))
            delete.grid(row=i + 1, column=3)
        window.update()

    def create_list():
        """
        Créer une nouvelle liste de tâches
        :return:
        """
        refresh_list()

    create_button = Button(name_frame, text="Créer une liste", command=create_list)
    create_button.pack(fill=X, anchor=N)
    name_frame.pack(fill=X, anchor=N)

    name_frame.pack(fill=X)

    refresh_list()
    list_frame.pack(fill=X)

    window.mainloop()


if __name__ == "__main__":
    task_config()
