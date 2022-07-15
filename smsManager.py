from ipaddress import IPv4Address  # for your IP address
import json
from pyairmore.request import AirmoreSession  # to create an AirmoreSession
from pyairmore.services.messaging import MessagingService  # to send messages

with open("config.json", "r") as f:
    config = json.load(f)

ip = IPv4Address(config["ip"])  # let's create an IP address object# now create a session
session = AirmoreSession(ip)  # create a session

service = MessagingService(session)  # create a MessagingService object


last_messages = {}


default_messages = [
    "Nous vous souhaitons une bonne partie !",
    "Tout les mélenchonistes sont morts, les zémouriens ont gagné !\nMerci de vous rendre immédiatement au point de rendez-vous !\n",
    "Merci de vous rendre immédiatement au point de rendez vous !",
    "Votre tâche"
]


def send_sms(phone_number: str, message: str):
    service.send_message(phone_number, message)
    print("SMS sent to {}".format(phone_number))


def get_new_messages(players: list):
    global last_messages
    messages = service.fetch_message_history()
    new_messages = []

    for message in messages:
        if message.phone not in [p.phone for p in players]:
            continue

        if is_sentence(message.content):
            continue

        if message.phone not in last_messages:
            last_messages[message.phone] = message
        elif message.datetime != last_messages[message.phone].datetime and not is_sentence(message.content):
            print("New message from {}: {}".format(message.phone, message.content))
            last_messages[message.phone] = message
            new_messages.append(message)
    return new_messages


def is_sentence(message: str):
    for sentence in default_messages:
        if sentence in message:
            return True
    return False
