import random


class WebGame:
    def __init__(self, ip: str, port: int):
        super().__init__()
        self.ip = ip
        self.port = port
        self.server = None
        self.receive = False


class Player:
    def __init__(self, used_passwords: list):
        self.tasks: list = []
        self.role: str = ""
        self.dead: bool = False
        self.asks: int = 0
        self.last_message: int = 0
        self.warnings: int = 0
        self.last_warning: int = 0
        self.id: str = "0"

        self.password: str = "".join([str(random.randint(0, 9)) for _ in range(8)])
        while self.password in used_passwords:
            self.password = "".join([str(random.randint(0, 9)) for _ in range(8)])
        used_passwords.append(self.password)

    def __repr__(self) -> str:
        """
        Affiche la classe Player telle qu'elle doit être déclarée pour ce joueur
        :return: str: Le string de l'affichage
        """
        return f"Player()"

    def get_str(self, game):
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
    def __init__(self, name: str, lastname: str, phone: str, used_passwords: list, used_ids: list):
        super().__init__(used_passwords)
        self.name: str = name
        self.lastname: str = lastname
        self.phone: str = phone

    def get_str(self, game) -> str:
        if game.game_master:
            if self.dead:
                return f"☠ {self.name} {self.lastname} ({game.config['names'][self.role]}): {show_phone_number(self.phone)}"
            return f"{self.name} {self.lastname} ({game.config['names'][self.role]}): {show_phone_number(self.phone)}"
        else:
            if self.dead and not game.config["show_dead_roles"]:
                return f"☠ {self.name} {self.lastname}: {show_phone_number(self.phone)}"
            elif self.dead:
                return f"☠ {self.name} {self.lastname} ({game.config['names'][self.role]}): {show_phone_number(self.phone)}"
        return f"{self.name} {self.lastname}: {show_phone_number(self.phone)}"


class WebPlayer(Player):
    def __init__(self, ip: str, nickname: str, color: str, used_passwords: list):
        super().__init__(used_passwords)
        self.ip: str = ip
        self.nickname: str = nickname
        self.color: str = color
        self.id: str = color

    def get_str(self, game: WebGame) -> str:
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


class BasicTask:
    type: str = "basic"

    def __init__(self, name: str, description: str, classe: str, location: str, other: dict = None):
        self.name: str = name
        self.description: str = description
        self.classe: str = classe
        self.location: str = location
        self.done: bool = False
        self.other: dict = other
        self.nb_given: int = 0
        self.success: int = 0

        if self.other and self.other.get("questions"):
            random.shuffle(self.other["questions"])
            questions = []
            for i in range(3):
                questions.append(self.other["questions"][i])
            self.other["questions"] = questions

    def __repr__(self):
        return f"{self.name} ({self.classe}): {self.description} | {self.location}"

    def __str__(self):
        return f"{self.name} ({self.classe})"


class ValidateBasicTask(BasicTask):
    type: str = "validate_basic"

    def __init__(self, name: str, description: str, classe: str, location: str, valid_keywords: list):
        super().__init__(name, description, classe, location, {})
        self.keywords: list = valid_keywords

    def __repr__(self):
        return f"ValidateBasicTask({self.name}, {self.description}, {self.classe}, {self.location}, {self.other})"

    def __str__(self):
        return f"Valide la tâche {self.name} ({self.classe})"


class ActivateBasicTask(BasicTask):
    type: str = "activate_basic"

    def __init__(self, name: str, description: str, classe: str, location: str, activ_keywords: list, message: str):
        super().__init__(name, description, classe, location, {})
        self.activ_keywords: list = activ_keywords
        self.message: str = message

    def __repr__(self):
        return f"ActivateBasicTask({self.name}, {self.description}, {self.classe}, {self.location}, {self.other})"

    def __str__(self):
        return f"Active la tâche {self.name} ({self.classe})"


class ActivValidTask(ValidateBasicTask):
    type: str = "activ_valid"

    def __init__(self, name: str, description: str, classe: str, location: str, valid_keywords: list,
                 activ_keywords: list, message: str):
        super().__init__(name, description, classe, location, valid_keywords)
        self.activ_keywords: list = activ_keywords
        self.message: str = message

    def __repr__(self):
        return f"ActivValidTask({self.name}, {self.description}, {self.classe}, {self.location}, {self.other})"

    def __str__(self):
        return f"Active et valide la tâche {self.name} ({self.classe})"


class CustomValidateTask(BasicTask):
    type: str = "custom_validate"

    def __init__(self, name: str, description: str, classe: str, location: str, valid_keywords: list, message: str):
        super().__init__(name, description, classe, location, {})
        self.keywords: list = valid_keywords
        self.message: str = message

    def __repr__(self):
        return f"CustomValidateTask({self.name}, {self.description}, {self.classe}, {self.location}, {self.other})"

    def __str__(self):
        return f"Valide la tâche {self.name} ({self.classe})"


# Show a phone number with "+33768330645" and "0768330645"
def show_phone_number(number: str) -> str:
    if number.startswith("+"):
        return f"{number[:3]} {number[3]} {number[4:6]} {number[6:8]} {number[8:10]} {number[10:]}"
    return f"{number[:2]} {number[2:4]} {number[4:6]} {number[6:8]} {number[8:]}"


if __name__ == "__main__":
    print(show_phone_number("+33768330645"))
