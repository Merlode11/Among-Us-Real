from instagrapi import Client

cl = Client()

user_ids: dict[str: int] = {}
with open("config.json", "r") as f:
    config = json.load(f)

cl.login(config["insta_username"], config["insta_password"])

def send_message(username, content): 
    user_id = user_ids.get(username)
    if not user_id: 
        user_id = cl.user_id_from_username(username)
        user_ids[username] = user_id
    cl.direct_send(content, user_ids=[user_id])

def get_new_messages() -> list: 
    pending_inbox = cl.direct_pending_inbox(20)
    messages = []
    for thread in pending_inbox: 
        for msg in thread.messages: 
            messages.append({
                username: find_username_by_id(msg.user_id),
                text: msg.text
            })
    return messages

def find_username_by_id(user_id): 
    for name, u_id in user_ids.items(): 
        if u_id == user_id: 
            return name
    return "none"

if __name__ == '__main__':
    print("Is Ready: " + str(isReady()))
    send_message("33767269602", "Hello World")
