# Twitch Bot Hunter

This little tool looks at Twitch accounts that are currently connected to a Twitch channel and cross references them with a list of known bots using [Twitch Insights](https://twitchinsights.net/bots).

Bots are _not_ banned by this tool, it just lists them.

==Please note that I haven't tested this on Linux or Windows yet, but in theory it should work there just fine.==

## Requirements

You need [Python 3](https://www.python.org/downloads/) to build this tool.

Please note that the following commands on __Windows__ might require you to use `python` instead of `python3` and `pip` instead of `pip3`, depending on your installation.

## Installation

Follow these instructions to build the tool.

__Step 1__: First let's upgrade `pip` to the newest stable version, this step is optional.

```
pip3 install --upgrade pip
```

It is recommended to run this tool in its own environment.

On __Linux__ and __macOS__:

```
cd path/to/bothunter
python3 -m venv .env
source .env/bin/activate
```

And on __Windows__ (assuming you run this in a PowerShell):

```
cd path/to/bothunter
python3 -m venv .env
.env/Scripts/Activate.ps1
```

__Step 2__: Then install requirements

```
pip3 install -r requirements.txt
```

__Step 3__: Run the tool

```
python3 -m bothunter <channel>
```

where `<channel>` is the name of the Twitch channel you want to use.

## Running the Tool

To run the tool after having been built, use the following steps.

**PLEASE NOTE:** Make sure to follow the upgrade described below under "Upgrade to Twitch API" to create a file named `.bothunter.conf` in the current directory, from where you run the program.


On __Linux__ and __macOS__:

```
cd path/to/bothunter
source .env/bin/activate
python3 -m bothunter <channel>
```


And on __Windows__:

```
cd path/to/bothunter
.env/Scripts/Activate.ps1
python3 -m bothunter <channel>
```


## Making a binary

This part is optional. Let's build a binary we can run directly.

```
pip3 install pyinstaller
pyinstaller cli.py --name=bothunter --onefile
```

After that, the binary is in `dist/bothunter` (or `dist/bothunter.exe` on Windows).

So instead of `python3 -m bothunter <channel>` you can now use `dist/bothunter <channel>`,
even _without_ activating the custom environment (step 1).

And of course that `bothunter` binary can be moved to any directory of your choice.


## Upgrade to Twitch API

Unfortunately the legacy API used to retrieve the list of chatters was disabled by Twitch as of April 2023 (see this [Blog Post](https://discuss.dev.twitch.tv/t/legacy-chatters-endpoint-shutdown-details-and-timeline-april-2023/43161)).

Therefore we have to use another API, which is more strict on who can use it. 

1. We have to create an access token linked to a user account, that has the moderator or broatcaster role on the channel we want to access.
1. Provide the username of a moderator account and the OAuth token when starting `bothunter`.

First you need to install or upgrade [Twitch-CLI](https://dev.twitch.tv/docs/cli/#twitch-cli-usage).

Next you have to get an [access token](https://dev.twitch.tv/docs/cli/token-command/):
```[bash]
$> twitch token -u -s moderator:read:chatters
```

The new version of `bothunter` requires three arguments.

- the channel name
- the username of a moderator account
- the OAuth token matching that moderator account

```[bash]
$> bothunter <channel> <username> <token>
```