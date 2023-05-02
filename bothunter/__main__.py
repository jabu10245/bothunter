from sys import exit, stderr
from argparse import ArgumentParser
from time import sleep
from signal import signal, SIGINT
from dataclasses import dataclass

from bothunter.twitch import get_broadcaster_id, get_moderator_id, get_twitch_chatters, refresh_token, ExpiredTokenException
from bothunter.insights import get_twitch_bots
from json import load, dump

# Add bots you want to allow here, so they don't end up listed as bots.
WHITELIST = [
    "soundalerts",
    "moobot",
    "wizebot",
    "nightbot",
    "streamelements",
    "own3d",
    "streamlabs",
    "buttsbot",
    "sery_bot",
    "blerp",
    "kofistreambot",
]

DEFAULT_INTERVAL_SECONDS = 3600  # one hour
CONFIG_FILENAME = '.bothunter.conf'

def find_bots(channel: str, broadcaster_id: int, moderator_id: int, access_token: str):
    """
    Retrieves a list of bots connected to that Twitch channel.
    """

    # Collect users currently connected to chat.
    usernames = set(get_twitch_chatters(broadcaster_id, moderator_id, access_token))
    if not usernames:
        print(f"Nobody is connected to {channel}.")
        return []

    # Remove WHITELIST bots:
    usernames = [user for user in usernames if user.lower() not in WHITELIST]

    # Collect a list of all known bots.
    bots = set(get_twitch_bots())
    return [user for user in usernames if user in bots]


def report_bots(channel: str, broadcaster_id: int, moderator_id: int, access_token: str, beep: bool):
    try:
        print("\nScanning…", file=stderr)
        bots = find_bots(channel, broadcaster_id, moderator_id, access_token)
        count = len(bots)
        bell = "\n\a\a" if beep else "\n"

        for bot in sorted(bots):
            print(bot)

        if not bots:
            print("No bots found :)", file=stderr)
        else:
            print(
                f"{bell}Found {count} bot" + ("s" if count > 1 else "") + ".",
                file=stderr,
            )
    except Exception as error:
        print(f"{bell}ERROR: {str(error)}", file=stderr)


def main():
    parser = ArgumentParser(
        prog="bothunter",
        description="Finds lurking bots connected to a Twitch channel.",
    )
    parser.add_argument(
        "channel", type=str, help="The name of the Twitch channel to scan"
    )
    parser.add_argument(
        "username", type=str, help="A username of a moderator account"
    )
    parser.add_argument(
        "token", type=str, help="The OAuth token to use"
    )
    parser.add_argument("-b", action="store_true", help="Beep when bots were found.")
    parser.add_argument(
        "-c", action="store_true", help="Continuously checking for bots."
    )
    parser.add_argument(
        "-i",
        metavar="<secs>",
        type=int,
        default=DEFAULT_INTERVAL_SECONDS,
        help=f"Scan interval in seconds. Defaults to {DEFAULT_INTERVAL_SECONDS}. Only used in combination with -c.",
    )

    args = parser.parse_args()
    channel = args.channel.lower()
    username = args.username.lower()
    token = args.token.lower()
    beep = args.b
    continuous = args.c
    seconds = args.i

    # handle ctrl-c properly
    def handle_ctrl_c(received, frame):
        print("\nbothunter stopped.", file=stderr)
        exit(0)

    signal(SIGINT, handle_ctrl_c)
    
    broadcaster_id = get_broadcaster_id(channel, token)
    if broadcaster_id is None:
        exit(1)

    moderator_id = get_moderator_id(username, token)
    if moderator_id is None:
        exit(1)

    # one-shot scan
    if not continuous:
        report_bots(channel, broadcaster_id, moderator_id, token, beep)
        exit(0)

    # continuous scan:
    while True:
        report_bots(channel, broadcaster_id, moderator_id, token, beep)
        sleep(seconds)


if __name__ == "__main__":
    main()
