from sys import stderr
import requests

def _get_twitch_user_id(login: str, client_id: str, token: str) -> int:
    url = f"https://api.twitch.tv/helix/users?login={login}"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}", "Client-ID": client_id})

    if response.status_code == 200:
        json = response.json()
        data = json['data'][0]
        id = data['id']
        return int(id)
    else:
        raise RuntimeError(f"HTTP status code {response.status_code} received.")

def get_broadcaster_id(channel: str, client_id: str, token: str) -> int:
    try:
        return _get_twitch_user_id(channel, client_id, token)
    except RuntimeError as e:
        print(f"Something went wrong, could not get the moderator ID for username {channel}, {str(e)}", file=stderr)
        return None

def get_moderator_id(username: str, client_id: str, token: str) -> int:
    try:
        return _get_twitch_user_id(username, client_id, token)
    except RuntimeError as e:
        print(f"Something went wrong, could not get the moderator ID for username {username}, {str(e)}", file=stderr)
        return None

def get_twitch_chatters(broadcaster_id: int, moderator_id: int, client_id: str, access_token: str):
    url = f"https://api.twitch.tv/helix/chat/chatters?{broadcaster_id=}&{moderator_id=}&first=1000"
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}", "Client-ID": client_id})

    if response.status_code == 200:
        json = response.json()
        chatters = list()
        if data := json.get('data'):
            for entry in data:
                if name := entry.get('user_name'):
                    chatters.append(name.lower())
        return chatters
    elif response.status_code == 401:
        print(f"Access denied. Make sure you own a valid access token.\nCheck your access token using 'twitch token -u -s moderator:read:chatters' and save it in the file named '.bothunter.conf'.", file=stderr)
        return []
    elif response.status_code == 403:
        print(f"Access denied. Make sure you are a moderator on that channel.", file=stderr)
        return []
    else:
        print(f"Something went wrong, could not get a list of chatters, HTTP status code {response.status_code} received.", file=stderr)
        return []