from sys import stderr
import requests

CLIENT_ID = "o6js7xyqkegojiokso246quvd0g29v"

class ExpiredTokenException(Exception):
    """ Twitch access token is expired. """

def refresh_token(client_id: str, client_secret: str, refresh_token: str) -> dict[str, str]:
    url = f"https://api.twitch.tv/oauth2/token"
    response = requests.post(url, f"grant_type=refresh_token&{refresh_token=}&{client_id=}&{client_secret}")

    if response.status_code == 200:
        json = response.json()
        return json
    else:
        print(f"HTTP status code {response.status_code} received: {response.text}")
        return None

def _get_twitch_user_id(login: str, access_token: str) -> int:
    url = f"https://api.twitch.tv/helix/users?login={login}"
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}", "Client-ID": CLIENT_ID})

    if response.status_code == 200:
        json = response.json()
        data = json['data'][0]
        id = data['id']
        return int(id)
    elif response.status_code == 401:
        raise RuntimeError(f"HTTP status code {response.status_code} received, your access token might be expired.")
    else:
        raise RuntimeError(f"HTTP status code {response.status_code} received.")

def get_broadcaster_id(channel: str, access_token: str) -> int:
    return _get_twitch_user_id(channel, access_token)

def get_moderator_id(username: str, access_token: str) -> int:
    return _get_twitch_user_id(username, access_token)

def get_twitch_chatters(broadcaster_id: int, moderator_id: int, access_token: str):
    url = f"https://api.twitch.tv/helix/chat/chatters?{broadcaster_id=}&{moderator_id=}&first=1000"
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}", "Client-ID": CLIENT_ID})

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