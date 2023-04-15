from sys import exit, stderr
from argparse import ArgumentParser
from time import sleep
from signal import signal, SIGINT
from dataclasses import dataclass

from bothunter.twitch import get_broadcaster_id, get_moderator_id, get_twitch_chatters
from bothunter.insights import get_twitch_bots
from json import load

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
    "Sery_Bot",
    "blerp",
    "kofistreambot",
]

DEFAULT_INTERVAL_SECONDS = 3600  # one hour

@dataclass
class Config:
    client_id: str
    username: str
    access_token: str
    refresh_token: str

def read_config() -> Config:
    filename = '.bothunter.conf'
    with open(filename) as file:
        json = load(file)
        
        return Config(
            client_id=json['client_id'],
            username=json['username'],
            access_token=json['access_token'],
            refresh_token=json['refresh_token']
        )


def find_bots(channel: str, broadcaster_id: int, moderator_id: int, config: Config):
    """
    Retrieves a list of bots connected to that Twitch channel.
    """

    # Collect users currently connected to chat.
    usernames = set(get_twitch_chatters(broadcaster_id, moderator_id, client_id=config.client_id, access_token=config.access_token))
    if not usernames:
        print(f"Nobody is connected to {channel}.")
        return []

    # Remove WHITELIST bots:
    usernames = [user for user in usernames if user not in WHITELIST]

    # Collect a list of all known bots.
    bots = set(get_twitch_bots())
    return [user for user in usernames if user in bots]


def report_bots(channel: str, broadcaster_id: int, moderator_id: int, config: Config, beep: bool):
    try:
        print("\nScanning…", file=stderr)
        bots = find_bots(channel, broadcaster_id, moderator_id, config)
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
    config = read_config()

    parser = ArgumentParser(
        prog="bothunter",
        description="Finds lurking bots connected to a Twitch channel.",
    )
    parser.add_argument(
        "channel", type=str, help="The name of the Twitch channel to scan"
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
    beep = args.b
    continuous = args.c
    seconds = args.i

    # handle ctrl-c properly
    def handle_ctrl_c(received, frame):
        print("\nbothunter stopped.", file=stderr)
        exit(0)

    signal(SIGINT, handle_ctrl_c)
    
    broadcaster_id = get_broadcaster_id(channel, config.client_id, config.access_token)
    if broadcaster_id is None:
        exit(1)

    moderator_id = get_moderator_id(config.username, config.client_id, config.access_token)
    if moderator_id is None:
        exit(1)

    # one-shot scan
    if not continuous:
        report_bots(channel, broadcaster_id, moderator_id, config, beep)
        exit(0)

    # continuous scan:
    while True:
        report_bots(channel, broadcaster_id, moderator_id, config, beep)
        sleep(seconds)


if __name__ == "__main__":
    main()
