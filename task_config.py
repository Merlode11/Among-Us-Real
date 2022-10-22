import json
import os
from tkinter import *
from tkinter import messagebox
from utils import clear_frame


def task_config():
    window = Tk()
    window.title("Configurer les tâches")
    window.geometry("800x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("amongus.ico")

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

    manageButton = Button(choiceListFrame, text="Gérer", command=manage_list_names)
    manageButton.grid(row=0, column=2)

    choiceListFrame.pack(fill=X, anchor=N)

    window.mainloop()


def create_task_list():
    window = Tk()
    window.title("Créer une liste de tâches")
    window.geometry("400x100")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("amongus.ico")

    nameFrame = Frame(window, bg="#f5f5f5")
    nameLabel = Label(nameFrame, text="Nom de la liste: ")
    nameEntry = Entry(nameFrame)
    nameLabel.grid(row=0, column=0)
    nameEntry.grid(row=0, column=1)

    nameFrame.pack(fill=X)

    def save_list():
        name = nameEntry.get()
        if name == "":
            messagebox.showerror("Erreur", "Le nom de la liste ne peut pas être vide")
            return
        if name in [liste.replace(".json", "") for liste in os.listdir("taskList") if liste.endswith(".json")]:
            messagebox.showerror("Erreur", "Une liste de tâches avec ce nom existe déjà")
            return
        with open(f"taskList/{name}.json", "w", encoding="utf-8") as file:
            json.dump([], file, indent=4, ensure_ascii=False)
        window.destroy()

    saveButton = Button(window, text="Enregistrer", command=save_list)
    saveButton.pack(side=BOTTOM)

    window.mainloop()


def manage_list_names():
    window = Tk()
    window.title("Gérer les noms de liste")
    window.geometry("400x600")
    window.resizable(True, True)
    window.configure(background='#f5f5f5')
    window.iconbitmap("amongus.ico")

    nameFrame = Frame(window, bg="#f5f5f5")
    titre = Label(nameFrame, text="Listes de tâches disponibles")
    titre.pack(fill=X, anchor=N)

    listFrame = Frame(window, bg="#f5f5f5")

    def refresh_list():
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

            def change_list(name):
                print(name)
                config["task_list"] = name
                with open("config.json", "w", encoding='utf8') as f:
                    json.dump(config, f, indent=4, ensure_ascii=False)
                refresh_list()

            def edit_list_name(name):
                edit_window = Tk()
                edit_window.title("Modifier le nom de la liste")
                edit_window.geometry("400x100")
                edit_window.resizable(True, True)
                edit_window.configure(background='#f5f5f5')
                edit_window.iconbitmap("amongus.ico")

                name_frame = Frame(edit_window, bg="#f5f5f5")
                nameLabel = Label(name_frame, text="Nom de la liste: ")
                nameEntry = Entry(name_frame)
                nameEntry.insert(0, name)
                nameLabel.grid(row=0, column=0)
                nameEntry.grid(row=0, column=1)

                nameFrame.pack(fill=X)

                def save_list():
                    new_name = nameEntry.get()
                    if new_name == "":
                        messagebox.showerror("Erreur", "Le nom de la liste ne peut pas être vide")
                        return
                    if new_name in [liste.replace(".json", "") for liste in os.listdir("taskList") if
                                    liste.endswith(".json")]:
                        messagebox.showerror("Erreur", "Une liste de tâches avec ce nom existe déjà")
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

            def del_list(name):
                if messagebox.askyesno("Supprimer la liste", "Voulez-vous vraiment supprimer cette liste ?"):
                    os.remove(f"taskList/{name}.json")
                    refresh_list()

            choose = Button(listFrame, text="Choisir", command=lambda task_name=task: change_list(f"{task_name}"))
            choose.grid(row=i + 1, column=1)
            edit = Button(listFrame, text="Modifier", command=lambda task_name=task: edit_list_name(f"{task_name}"))
            edit.grid(row=i + 1, column=2)
            delete = Button(listFrame, text="Supprimer", command=lambda task_name=task: del_list(f"{task_name}"))
            delete.grid(row=i + 1, column=3)
        window.update()

    def create_list():
        create_task_list()
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
