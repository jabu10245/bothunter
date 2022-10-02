from sys import stderr
import requests

def get_twitch_chatters(channel: str):
    """
    Retrieve a list of user names connected to the chat in this channel.
    """

    url = f"https://tmi.twitch.tv/group/user/{channel}/chatters"
    response = requests.get(url, headers={"Accept": "application/json"})

    if response.status_code == 200:
        json = response.json()
        if chatters := json.get('chatters'):
            # not interested in VIPs, mods, etc
            return [username.lower() for username in chatters.get("viewers")]
        print(f"No bots were found on the {channel}.", file=stderr)
    else:
        print(f"Something went wrong, could not get a list of chatters, HTTP status code {response.status_code} received.", file=stderr)
    print(f"Nobody connected to {channel}", file=stderr)
    return []