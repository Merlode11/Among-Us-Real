from tkinter import messagebox, ttk
from smsManager import send_sms


class Command:
    def __init__(self, 
    name: str, 
    description: str, 
    aliases: list,
    usage: str,
    exemple: str,
    permission: str = None):
        self.name = name
        self.description = description
        self.aliases = aliases
        self.usage = usage
        self.exemple = exemple
        self.permission = permission
 
        
    def get_help(self, config: dict = None):
        """
        Show the help message for the command
        """
        string: str = "Voici la page d'aide pour la commande " + self.name + ":"
        string += "\n" + self.description
        string += "\nAlias :" + ", ".join(self.aliases)
        if self.permission: 
            string += "\nUtilisable par :"
            if config is not None and config.get("names") and config["names"].get(self.permission.lower()):
                string += config["names"][self.permission.lower()]
            else: 
                string += self.permission
        string += "\nUtilisation:" + self.usage + " (" + self.exemple + ")"
        return string
    
    def execute(self, player, message):
        pass
    
    def run(self, player, message, game):
        # Check permission
        if self.permission and player.role != self.permission:
            perm:str = self.permission
            if config.get("names") and config["names"].get(self.permission.lower()):
                perm = config["names"][self.permission.lower()]
                  
            send_sms(player.phone, "Vous ne pouvez pas utiliser cette commande car vous n'êtes pas" + perm + " !")
            return True
        if game.pause and self.name != "help":
            send_sms(player.phone, "La partie est actuellement en pause. Vous ne pouvez pas faire de commandes")
            
        self.execute(player, message, game)
        return True

commands: list = []

def task_func(command, player, message, game): 
    try:
        task_number = int(message.split(" ")[1])
        task = player.tasks[task_number - 1]
        string = f"{task.name} ({task.classe})\n"
        string += f"Lieu: {task.location}\n"
        string += f"Description: {task.description}\n"
        send_sms(player.phone, string)
    except:
        send_sms(player.phone, "Veuillez entrer un numéro de tâche valide !")

task = Command("task", "Permet de voir la description d'une tâche", ["tâche", "détail", "detail", "task", "tache"], "task NOMBRE", "task 1")
task.execute = task_func

commands.append(task)

def info_func(command, player, message, game): 
    remining = 0
    done = 0
    string = ""
    for i in range(len(player.tasks)):
        task = player.tasks[i]
        if task.done:
            done += 1
        else:
            remining += 1
            string += f"{i + 1}: {task.name} ({task.classe})\n"
        string = f"Il vous reste {remining} tâches à accomplir.\n" + string
        if done == len(player.tasks):
            string += "Vous avez accompli toutes vos tâches !\n"

        string += f"Il reste {len(self.done_tasks)}/{self.given_tasks} tâche pour les " + game.config["names"]["crewmate"]+ "."
    send_sms(player.phone, string)
    
info = Command("info", "Permet de voir les tâches restantes", ["restant", "last", "reste"], "info", "info")

info.execute = info_func

commands.append(info)

def deads_func(command, player, message, game): 
    if player.asks >= game.config["max_dead_check"]:
        send_sms(player.phone, "Vous avez utilisé toutes vos demandes !")
    else:
        states = "Voici les états de chaque joueur:\n"
        for joueur in self.players:
            if joueur.dead:
                states += "- " + joueur.name + " " + joueur.lastname + " (mort)\n"
            else:
                states += "- " + joueur.name + " " + joueur.lastname + " (vivant)\n"
        player.asks += 1
        states += "\n Il vous reste " + str(game.config["max_dead_check"] - player.asks) + "/" + str(game.config["max_dead_check"]) + " demandes."
        send_sms(player.phone, states)

deads = Command("deads", "Voir les états de chaque joueur", ["view", "states", "états", "morts"], "deads", "deads", "scientist")

deads.execute = deads_func

commands.append(deads)

def mort_func(command, player, message, game):
    if game.game_master: 
        response = messagebox.askokcancel("Mort détecté",
        f"{player.name} {player.lastname} découvert un corps ! Son message est :\n {message}")
        if response == "ok":
            game.send_message_to_all(
              "Un cadavre a été signalé.\nMerci de vous rendre immédiatement au point de rendez vous !")
        elif response == "cancel":
            send_sms(player.phone, "Votre demande a été refusée par l'organisateur.ice")
    else: 
        dead_str = message.split(" ")[1:]
        try:
            dead_id = player_str[0] - 1
            dead = game.players[player_id]
            if not player.dead: 
                send_sms(player.phone, "Ce joueur ne peux pas être déclaré comme cadavre car il n'est pas mort")
                return
            elif :
            

mort = Command("mort", "Annonce à l'organisateur la découverte d'un corps", ["death", "cadavre", "corps"], "mort PERSONNE")

mort.execute = mort_func

def done_func(command, player, message, game): 
    try:
        task_number = int(message.split(" ")[1])
        task = player.tasks[task_number - 1]
        if task.done:
            send_sms(player.phone, "Vous avez déjà déclaré avoir fait la tâche " + str(task_number))
        else:
            task.done = True
            game.done_tasks.append(task)
            send_sms(player.phone, f"Votre tâche {task.name} a été confirmée comme faite !")
            messagebox.showinfo("Succès",
                  f"{player.name} {player.lastname} a confirmé avoir réalisé la tâche {task.name} ! Son message est :\n {message}")
    except:
        send_sms(player.phone, "Veuillez entrer un numéro de tâche valide !")

done = Command("done", "Valide une tâche comme faite", ["fait", "réalisé"], "done NOMBRE", "done 1")

done.execute = done_func

commands.append(done)

def help_func(command, player, message, game):
    if len(message.split(" ")) == 1: 
        string = "Voici toutes les commandes disponibles:\n"
        for command in commands:
            string += command.exemple + ": " + command.description
        send_sms(player.phone, string)
    else:
        command_str = message.split(" ")[1]
        command = None
        for cmd in commands:
            if command_str in ([cmd.name] + cmd.aliases): 
                command = cmd
                break
        string = command.get_help(game.config)
        send_sms(player.phone, string)

help_cmd = Command("help", "Obtenir toutes les commandes et de l'aide pour chacune", ["aide", "commandes", "commande", "commands", "command"], "help (COMMANDE)", "help help")

help_cmd.execute = help_func

commands.append(help_cmd)
