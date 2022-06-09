from sys import stderr, argv
from argparse import ArgumentParser

from bothunter.twitch import get_twitch_chatters
from bothunter.insights import get_twitch_bots

# Add bots you want to allow here, so they don't end up listed as bots.
WHITELIST = ["soundalerts", "moobot", "wizebot", "nightbot", "streamelements", "own3d", "streamlabs",
 "buttsbot"]

def find_bots(channel: str):
    """
    Retrieves a list of bots connected to that Twitch channel.
    """

    # Collect users currently connected to chat.
    usernames = set(get_twitch_chatters(channel))
    if len(usernames) < 1:
        return []
    
    # Collect a list of all known bots.
    bots = set(get_twitch_bots())
    if len(bots) < 1:
        return []
    
    # Collect bots connected to chat.
    found_bots = list()
    for username in usernames:
        if username in bots and not username in WHITELIST:
            found_bots.append(username)
    
    return found_bots

def main():
    parser = ArgumentParser(prog="bothunter", description="Finds lurking bots connected to a Twitch channel.")
    parser.add_argument("channel", type=str, help="The name of the Twitch channel to scan")
    
    args = parser.parse_args()
    channel = args.channel.lower()
    bots = find_bots(channel)
    count = len(bots)

    for bot in sorted(bots):
        print(bot)
    if count == 0:
        print("No bots found :)", file=stderr)
    elif count == 1:
        print("\n\a\aFound 1 bot.", file=stderr)
    else:
        print(f"\n\a\aFound {count} bots.", file=stderr)

if __name__ == "__main__":
    main()