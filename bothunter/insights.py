from sys import stderr
import requests


URL = "https://api.twitchinsights.net/v1/bots/all"

def get_twitch_bots():
    """
    Retrieve a list of known bots.
    """

    response = requests.get(URL, headers={"Accept": "application/json"})

    if response.status_code == 200:
        json = response.json()
        if botsJSON := json.get("bots"):
            return [name.lower() for (name, _, _) in botsJSON]
        print("The bot list was empty - check service settings/status on the twitchinsights.net!", file=stderr)
    else:
        print(f"Something went wrong, could not get a list of bots, HTTP status code {response.status_code} received.", file=stderr)
    return []