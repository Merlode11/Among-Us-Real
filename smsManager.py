from ipaddress import IPv4Address  
import json
from pyairmore.request import AirmoreSession
from pyairmore.services.messaging import MessagingService
from tkinter import messagebox

with open("config.json", "r") as f:
    config = json.load(f)

ip = IPv4Address(config["ip"])

session = AirmoreSession(ip)

service = MessagingService(session)


last_messages = {}
sent_messages = {}


def send_sms(phone_number: str, message: str):
    """
    Envoye un SMS au numéro de téléphone spécifié
    """
    sent_messages[phone_number] = message
    service.send_message(phone_number, message)
    print("SMS sent to {}".format(phone_number))


def get_new_messages(game) -> list:
    """
    Renvoie tous les nouveaux messages detectés
    """
    players = game.players
    global last_messages
    global sent_messages
    messages = service.fetch_message_history()
    new_messages = []

    for message in messages:
        if message.phone not in [p.phone for p in players]:
            continue

        if message.phone not in last_messages:
            last_messages[message.phone] = message
        elif message.datetime != last_messages[message.phone].datetime and sent_messages[message.phone] != message.content:
            print("New message from {}: {}".format(message.phone, message.content))
            player = [p for p in players if p.phone == message.phone][0]
            last_messages[message.phone] = message
            new_messages.append(message)
            player.last_message = message.datetime
            if player.warnings >= 1: 
                if game.pause and player.warnings >= game.config["max_warns"]:
                    game.pause = False
                    game.send_message_to_all(f"{player.name} {player.lastname} a refait surface, plus besoin de s'inquiéter. La partie reprend !")
                    if game.config.game_master:
                        messagebox.showinfo("La partie reprend", f"{player.name} {player.lastname} a refait surface. La partie reprends")
                player.warnings = 0
    return new_messages
