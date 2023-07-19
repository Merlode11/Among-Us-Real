import random
from datetime import datetime


class Player:
    def __init__(self, used_passwords: list, used_id: list):
        self.tasks: list = []
        self.role: str = ""
        self.dead: bool = False
        self.asks: int = 0
        self.last_message: int = int(datetime.now().timestamp())
        self.warnings: int = 0
        self.last_warning: int = int(datetime.now().timestamp())
        self.id: str = "0"
        self.popup: str or None = None

        self.password: str = "".join([str(random.randint(0, 9)) for _ in range(8)])
        while self.password in used_passwords:
            self.password = "".join([str(random.randint(0, 9)) for _ in range(8)])
        used_passwords.append(self.password)

        player_id = random.randint(0, 999)
        while player_id in used_id:
            player_id = random.randint(0, 999)
        used_id.append(player_id)
        self.id = f"{player_id:03}"

    def __repr__(self) -> str:
        """
        Affiche la classe Player telle qu'elle doit être déclarée pour ce joueur
        :return: str: Le string de l'affichage
        """
        return f"Player()"

    def get_str(self, game):
        """
        Renvoie un affichage du joueur afin de l'afficher dans la fenêtre de la partie
        :param game: Game: La partie actuelle
        :return: str: L'affichage de l'identité du joueur
        """
        pass

    def get_name(self) -> str:
        """
        Renvoie l'affichage du nom du joueur pour les autres joueurs
        :return: str: Le nom du joueur
        """
        pass

    def finished_all_tasks(self) -> bool:
        """
        Renvoie si le joueur a fini toutes ses tâches
        :return: bool: True s'il a fini toutes ses tâches, False sinon
        """
        finished = 0
        for task in self.tasks:
            if task.done:
                finished += 1
        return finished == len(self.tasks)


class SMSPlayer(Player):
    def __init__(self, name: str, phone: str, used_passwords: list, used_id: list):
        super().__init__(used_passwords, used_id)
        self.name: str = name
        self.phone: str = phone

    def get_str(self, game) -> str:
        """
        Renvoie un affichage du joueur afin de l'afficher dans la fenêtre de la partie
        :param game: Game: La partie actuelle
        :return: str: L'affichage de l'identité du joueur
        """
        if game.game_master:
            if self.dead:
                return f"☠ {self.name} ({game.config['names'][self.role]}): \
                {show_phone_number(self.phone)} "
            return f"{self.name} ({game.config['names'][self.role]}): {show_phone_number(self.phone)}"
        else:
            if self.dead and not game.config["show_dead_roles"]:
                return f"☠ {self.name}: {show_phone_number(self.phone)}"
            elif self.dead:
                return f"☠ {self.name} ({game.config['names'][self.role]}): \
                {show_phone_number(self.phone)}"
        return f"{self.name}: {show_phone_number(self.phone)}"

    def get_name(self) -> str:
        """
        Renvoie l'affichage du nom du joueur pour les autres joueurs
        :return: str: Le nom du joueur
        """
        return self.name


class WebPlayer(Player):
    def __init__(self, ip: str, nickname: str, color: str, used_passwords: list, used_id: list):
        super().__init__(used_passwords, used_id)
        self.ip: str = ip
        self.nickname: str = nickname
        self.color: str = color

    def get_str(self, game) -> str:
        """
        Renvoie un affichage du joueur afin de l'afficher dans la fenêtre de la partie
        :param game: Game: La partie actuelle
        :return: str: L'affichage de l'identité du joueur
        """
        if game.game_master:
            if self.dead:
                return f"☠ {self.nickname} ({self.ip}), {game.config['names'][self.role]}"
            return f"{self.nickname} ({self.ip}), {game.config['names'][self.role]}"
        else:
            if self.dead and not game.config["show_dead_roles"]:
                return f"☠ {self.nickname} ({self.ip})"
            elif self.dead:
                return f"☠ {self.nickname} ({self.ip}), {game.config['names'][self.role]}"
        return f"{self.nickname} ({self.ip})"

    def get_name(self) -> str:
        """
        Renvoie l'affichage du nom du joueur pour les autres joueurs
        :return: str: Le nom du joueur
        """
        return self.nickname


class InstaPlayer(Player):
    def __init__(self, name: str, username: str, used_passwords: list, used_id: list):
        super().__init__(used_passwords, used_id)
        self.name: str = name
        self.username: str = username

    def get_str(self, game) -> str:
        """
        Renvoie un affichage du joueur afin de l'afficher dans la fenêtre de la partie
        :param game: Game: La partie actuelle
        :return: str: L'affichage de l'identité du joueur
        """
        if game.game_master:
            if self.dead:
                return f"☠ {self.name} ({game.config['names'][self.role]}): \
                {self.username} "
            return f"{self.name} ({game.config['names'][self.role]}): {self.username}"
        else:
            if self.dead and not game.config["show_dead_roles"]:
                return f"☠ {self.name}: {self.username}"
            elif self.dead:
                return f"☠ {self.name} ({game.config['names'][self.role]}): \
                {self.username}"
        return f"{self.name}: {self.username}"

    def get_name(self) -> str:
        """
        Renvoie l'affichage du nom du joueur pour les autres joueurs
        :return: str: Le nom du joueur
        """
        return f"{self.name}"


class BasicTask:
    type: str = "basic"

    def __init__(self, name: str, description: str, steps: int, location: str):
        self.name: str = name
        self.description: str = description
        self.steps: int = steps
        self.location: str = location
        self.done: bool = False
        self.nb_given: int = 0
        self.success: int = 0

    def __repr__(self):
        return f"{self.name} ({self.steps}): {self.description} | {self.location}"

    def __str__(self):
        return f"{self.name} ({self.steps})"
    
    def to_dict(self) -> dict: 
        """
        Renvoie la tâche sous forme de dictionnaire
        """
        return {
            "type": "basic",
            "name": self.name,
            "description": self.description,
            "steps": self.steps,
            "location": self.location,
            "done": self.done,
        }

    # JSON serializable
    def __json__(self):
        return self.to_dict()


class ValidateBasicTask(BasicTask):
    type: str = "validate_basic"

    def __init__(self, name: str, description: str, steps: int, location: str, valid_keywords: list):
        super().__init__(name, description, steps, location)
        self.keywords: list = valid_keywords

    def __repr__(self):
        return f"ValidateBasicTask({self.name}, {self.description}, {self.steps}, {self.location})"

    def __str__(self):
        return f"{self.name} ({self.steps})"

    def to_dict(self) -> dict:
        """
        Renvoie la tâche sous forme de dictionnaire
        """
        return {
            "type": "validate_basic",
            "name": self.name,
            "description": self.description,
            "steps": self.steps,
            "location": self.location,
            "keywords": self.keywords,
            "done": self.done,
        }


class ActivateBasicTask(BasicTask):
    type: str = "activate_basic"

    def __init__(self, name: str, description: str, steps: int, location: str, activ_keywords: list, message: str):
        super().__init__(name, description, steps, location)
        self.activ_keywords: list = activ_keywords
        self.message: str = message
        self.active: bool = False

    def __repr__(self):
        return f"ActivateBasicTask({self.name}, {self.description}, {self.steps}, {self.location})"

    def __str__(self):
        return f"{self.name} ({self.steps})"

    def to_dict(self) -> dict:
        """
        Renvoie la tâche sous forme de dictionnaire
        """
        return {
            "type": "activate_basic",
            "name": self.name,
            "description": self.description,
            "steps": self.steps,
            "location": self.location,
            "activ_keywords": self.activ_keywords,
            "message": self.message,
            "active": self.active,
            "done": self.done,
        }


class ActivValidTask(ValidateBasicTask):
    type: str = "activ_valid"

    def __init__(self, name: str, description: str, steps: int, location: str, valid_keywords: list,
                 activ_keywords: list, message: str):
        super().__init__(name, description, steps, location, valid_keywords)
        self.activ_keywords: list = activ_keywords
        self.message: str = message
        self.active: bool = False

    def __repr__(self):
        return f"ActivValidTask({self.name}, {self.description}, {self.steps}, {self.location})"

    def __str__(self):
        return f"{self.name} ({self.steps})"

    def to_dict(self) -> dict:
        """
        Renvoie la tâche sous forme de dictionnaire
        """
        return {
            "type": "activ_valid",
            "name": self.name,
            "description": self.description,
            "steps": self.steps,
            "location": self.location,
            "keywords": self.keywords,
            "activ_keywords": self.activ_keywords,
            "message": self.message,
            "active": self.active,
            "done": self.done,
        }


def set_task(task_dict: dict) -> BasicTask or ActivateBasicTask or ValidateBasicTask or ActivValidTask:
    """
    Créer un object caractérisant une classe spéciale de tâche et le renvoie
    """
    if task_dict.get("type") == "basic":
        return BasicTask(task_dict.get("name", ""), task_dict.get("description", ""), task_dict.get("steps", 1), task_dict.get("location", ""))
    elif task_dict.get("type") == "validate_basic":
        return ValidateBasicTask(task_dict.get("name", ""), task_dict.get("description", ""), task_dict.get("steps", 1),
                                 task_dict.get("location", ""),
                                 task_dict.get("keywords", []))
    elif task_dict.get("type") == "activate_basic":
        return ActivateBasicTask(task_dict.get("name", ""), task_dict.get("description", ""), task_dict.get("steps", 1),
                                 task_dict.get("location", ""),
                                 task_dict.get("activ_keywords", []), task_dict.get("message", ""))
    elif task_dict.get("type") == "activ_valid":
        return ActivValidTask(task_dict.get("name", ""), task_dict.get("description", ""), task_dict.get("steps", 1), task_dict.get("location", ""),
                              task_dict.get("keywords", []), task_dict.get("activ_keywords", []), task_dict.get("message", ""))


# Show a phone number with "+33768330645" and "0768330645"
def show_phone_number(number: str) -> str:
    if number.startswith("+"):
        return f"{number[:3]} {number[3]} {number[4:6]} {number[6:8]} {number[8:10]} {number[10:]}"
    elif number.startswith("00"): 
        return f"{number[:2]} {number[2:4]} {number[4]} {number[5:7]} {number[7:9]} {number[9:11]} {number[11:]}"
    return f"{number[:2]} {number[2:4]} {number[4:6]} {number[6:8]} {number[8:]}"


if __name__ == "__main__":
    print(show_phone_number("+33768330645"))
