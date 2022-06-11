from sys import exit, stderr
from argparse import ArgumentParser
from time import sleep
from signal import signal, SIGINT

from bothunter.twitch import get_twitch_chatters
from bothunter.insights import get_twitch_bots

# Add bots you want to allow here, so they don't end up listed as bots.
WHITELIST = ["soundalerts", "moobot", "wizebot", "nightbot", "streamelements", "own3d", "streamlabs",
 "buttsbot"]

DEFAULT_INTERVAL_SECONDS = 3600 # one hour

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

def report_bots(channel: str, beep: bool):
    print("\nScanning…", file=stderr)
    bots = find_bots(channel)
    count = len(bots)
    bell = "\a\a" if beep else ""

    for bot in sorted(bots):
        print(bot)
    
    if count == 0:
        print("No bots found :)", file=stderr)
    elif count == 1:
        print(f"\n{bell}Found 1 bot.", file=stderr)
    else:
        print(f"\n{bell}Found {count} bots.", file=stderr)

def main():
    parser = ArgumentParser(prog="bothunter", description="Finds lurking bots connected to a Twitch channel.")
    parser.add_argument("channel", type=str, help="The name of the Twitch channel to scan")
    parser.add_argument("-b", action="store_true", help="Beep when bots were found.")
    parser.add_argument("-c", action="store_true", help="Continuously checking for bots.")
    parser.add_argument("-i", metavar="<secs>", type=int, default=DEFAULT_INTERVAL_SECONDS, help=f"Scan interval in seconds. Defaults to {DEFAULT_INTERVAL_SECONDS}. Only used in combination with -c.")
    
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

    # one-shot scan
    if not continuous:
        report_bots(channel, beep)
        exit(0)

    # continuous scan:
    while True:
        report_bots(channel, beep)
        sleep(seconds)

if __name__ == "__main__":
    main()