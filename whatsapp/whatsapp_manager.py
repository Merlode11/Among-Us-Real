import requests


def sendRequest(action, data) -> dict or str:
    received = requests.post("http://localhost:3045/" + action, json=data)
    if received.headers["Content-Type"] == "application/json":
        return received.json()
    else:
        return received.text


def send_message(phoneNumber, content, options=None):
    if options is None:
        options = {}
    if len(phoneNumber) < 11:
        phoneNumber = "33" + phoneNumber if not phoneNumber.startswith("0") else "33" + phoneNumber[1:]
    if not phoneNumber.endswith("@c.us"):
        phoneNumber += "@c.us"
    phoneNumber = phoneNumber.replace("+", "")

    if options.get("quotedMessageId", None):
        if type(options["quotedMessageId"]) == dict:
            options["quotedMessageId"] = options["quotedMessageId"].get("_serialized")

    return send_message_raw(phoneNumber, content, options)


def send_message_raw(chatId, content, options={}):
    data = {
        "chatId": chatId,
        "content": content,
        "options": options,
    }
    return sendRequest("send_message", data)


def send_seen(chatId):
    data = {
        "chatId": chatId,
    }
    return sendRequest("sendSeen", data)


def send_typing(chatId, state):
    data = {
        "chatId": chatId,
        "state": state,
    }
    return sendRequest("sendTyping", data)


def is_ready() -> bool:
    data = {}
    infos = sendRequest("getState", data)
    return infos == "CONNECTED"


def get_user() -> dict:
    received = requests.get("http://localhost:3045/@me")
    if received.headers["Content-Type"] == "application/json":
        return received.json()
    else:
        return received.text


if __name__ == '__main__':
    print("Is Ready: " + str(is_ready()))
    send_message("33767269602", "Hello World")
