from instagrapi import Client

cl = Client()

user_infos: dict[int: dict] = {}

with open("config.json", "r") as f:
    config = json.load(f)

cl.login(config["insta_username"], config["insta_password"])

def send_message(username, content): 
    infos = find_id_by_username(username)
    if not user_id: 
        infos = cl.user_info_by_username(username).dict()
        user_infos[infos["pk"]] = infos
    cl.direct_send(content, user_ids=[infos["pk"]])

def get_new_messages() -> list: 
    pending_inbox = cl.direct_pending_inbox(20)
    messages = []
    for thread in pending_inbox: 
        for msg in thread.messages: 
            infos = user_infos.get(msg.user_id, {})
            messages.append({
                "username": infos.get("username"),
                "text": msg.text,
                "full_name": infos.get("full_name")
                
            })
    return messages

def find_id_by_username(username): 
    for u_id, infos in user_infos.items(): 
        if infos["username"] == username: 
            return u_id
    return None

if __name__ == '__main__':
    print("Is Ready: " + str(isReady()))
    send_message("33767269602", "Hello World")
