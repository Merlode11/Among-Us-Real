from instagrapi import Client
import json
import datetime

cl = Client()

user_infos: dict[int: dict] = {}

read_messages = []

time_now = datetime.datetime.now()

with open("config.json", "r") as f:
    config = json.load(f)

cl.login(config["insta_username"], config["insta_password"])


def send_message(username, content):
    user_id = find_id_by_username(username)
    if not user_id:
        infos = cl.user_info_by_username(username).dict()
        user_infos[infos["pk"]] = infos
        user_id = infos["pk"]
    cl.direct_send(content, user_ids=[int(user_id)])


def get_new_messages() -> list:
    pending_inbox = cl.direct_threads(selected_filter="unread", thread_message_limit=2)
    pending_inbox.extend(cl.direct_pending_inbox())
    messages = []
    for thread in pending_inbox:
        for msg in thread.messages:
            if msg.id in read_messages:
                continue
            if msg.is_sent_by_viewer:
                continue
            if msg.text is None:
                continue
            infos = user_infos.get(f"{msg.user_id}", {})
            if not infos:
                infos = cl.user_info(user_id=f"{msg.user_id}").dict()
                user_infos[infos["pk"]] = infos
            messages.append({
                "username": infos.get("username"),
                "text": msg.text,
                "full_name": infos.get("full_name")
            })
            read_messages.append(msg.id)
    return messages


def find_id_by_username(username):
    for u_id, infos in user_infos.items():
        if infos["username"] == username:
            return u_id
    return None


if __name__ == '__main__':
    send_message("merlode11", "test")
    get_new_messages()
