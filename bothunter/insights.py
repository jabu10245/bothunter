from sys import stderr
import requests

URL = "https://api.twitchinsights.net/v1/bots/all"
def get_twitch_bots():
    """
    Retrieve a list of known bots.
    """

    url = f"https://api.twitchinsights.net/v1/bots/all"
    response = requests.get(url, headers={"Accept": "application/json"})

    if response.status_code == 200:
        json = response.json()
        if "bots" in json:
            botsJSON = json["bots"]
            return [name.lower() for (name, _, _) in botsJSON]

    else:
        print(f"Something went wrong, could not get a list of bots, HTTP status code {response.status_code} received.", file=stderr)
        return []
    
    print("Something went wrong. Could not retrieve a list of bots from twitchinsights.net!", file=stderr)
    return []