from ipaddress import IPv4Address  
import json
from pyairmore.request import AirmoreSession
from pyairmore.services.messaging import MessagingService
from pyairmore.data.messaging import MessageType
from tkinter import messagebox
from time import sleep

with open("config.json", "r") as f:
    config = json.load(f)

ip = IPv4Address(config["ip"])

session = AirmoreSession(ip)

service = MessagingService(session)


last_messages = {}


def send_sms(phone_number: str, message: str):
    """
    Envoye un SMS au numéro de téléphone spécifié
    """
    try:
        service.send_message(phone_number, message)
    except Exception as e:
        print(e)
        sleep(2)
        send_sms(phone_number, message)


def get_new_messages(game) -> list:
    """
    Renvoie tous les nouveaux messages detectés
    """
    players = game.players
    global last_messages
    messages = service.fetch_message_history()
    new_messages = []

    for message in messages:
        if message.phone not in [p.phone for p in players]:
            continue

        if message.phone not in last_messages:
            last_messages[message.phone] = message
        elif message.datetime != last_messages[message.phone].datetime and message.type == MessageType.RECEIVED:
            print("New message from {}: {}".format(message.phone, message.content))
            player = [p for p in players if p.phone == message.phone][0]
            last_messages[message.phone] = message
            new_messages.append(message)
            player.last_message = message.datetime.timestamp()
            if player.warnings >= 1: 
                if game.pause and player.warnings >= game.config["max_warns"]:
                    game.pause = False
                    game.send_message_to_all(f"{player.name} {player.lastname} a refait surface, plus besoin de "
                                             f"s'inquiéter. La partie reprend !")
                    if game.config.game_master:
                        messagebox.showinfo("La partie reprend", f"{player.name} {player.lastname} a refait surface. "
                                                                 f"La partie reprends")
                player.warnings = 0
    return new_messages
