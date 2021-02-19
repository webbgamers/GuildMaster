# GuildMaster
This is a WIP bot designed to take the difficulty out of managing your server. The name is temporary while I try to come up with a better name.

## Planned Features
* Profanity filtering
* XP/leveling system
* Customizable auto-responses
* Moderation commands such as warning, kicking, etc
* Server logs
* Message management commands such as move and purge
* Per-channel settings
* Hopefully more

## Running Yourself With Docker
### Requirements
* [Docker](https://www.docker.com/products/docker-desktop)
### Instructions
* Clone or download this repo to wherever you want.
* Create a python file named `Secrets.py` with a `get_token()` function that returns your bot token and a `get_db_uri()` function that returns the MongoDB connection URI. An example file called `SecretsExample.py` is in the repository for you to copy/rename and just requires you to replace the text `YOUR_BOT_TOKEN` with your actual bot token.
NOTE: This method of storing secrets is subject to change.
* Open the shell of your choice in the repository's folder.
* Run `docker-compose up -d`.
* Docker should build GuildMaster and download the [`mongo`](https://hub.docker.com/_/mongo/) Docker image and run them together.
* Running `docker ps` should show at least two containers, one named `guildmaster_guildmaster_1` based on the `guildmaster` image, and one named `guildmaster_mongodb_1` based on the `mongo` image.

## Credits
* [webbgamers](https://github.com/webbgamers) (Developer)
* [discord.py](https://github.com/Rapptz/discord.py) (API wrapper)
* [Contributors](https://github.com/webbgamers/GuildMaster/graphs/contributors) (Great People)
