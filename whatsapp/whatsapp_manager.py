from flask import Flask, request
import requests

def sendRequest(action, data):
    received = requests.post("http://localhost:3045/" + action, json=data)
    if received.headers["Content-Type"] == "application/json":
        return received.json()
    else:
        return received.text


def sendMessage(phoneNumber, content, options={}):
    if len(phoneNumber) < 11:
        phoneNumber = "33" + phoneNumber if not phoneNumber.startswith("0") else "33" + phoneNumber[1:]
    if not phoneNumber.endswith("@c.us"):
        phoneNumber += "@c.us"
    phoneNumber = phoneNumber.replace("+", "")

    if options.get("quotedMessageId", None):
        if type(options["quotedMessageId"]) == dict:
            options["quotedMessageId"] = options["quotedMessageId"].get("_serialized")

    return sendMessageRaw(phoneNumber, content, options)


def sendMessageRaw(chatId, content, options={}):
    data = {
        "chatId": chatId,
        "content": content,
        "options": options,
    }
    sendRequest("sendMessage", data)


def sendSeen(chatId):
    data = {
        "chatId": chatId,
    }
    sendRequest("sendSeen", data)


def sendTyping(chatId, state):
    data = {
        "chatId": chatId,
        "state": state,
    }
    sendRequest("sendTyping", data)


def isReady():
    data = {}
    infos = sendRequest("getState", data)
    return infos == "CONNECTED"


if __name__ == '__main__':
    print("Is Ready: " + str(isReady()))
    sendMessage("33767269602", "Hello World")
