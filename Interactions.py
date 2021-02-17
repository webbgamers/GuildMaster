from discord.ext import commands
import requests


class Interactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    # Listen for raw socket messages
    async def on_socket_response(self, msg):
        # Handle interaction if socket message is interaction
        if msg.get("t") == "INTERACTION_CREATE":
            data = msg.get("d")
            token = data.get("token")
            member = data.get("member")
            id = data.get("id")
            guild_id = data.get("guild_id")
            command = data.get("data")
            channel_id = data.get("channel_id")

            # Pog command
            if command.get("name") == "pog":
                url = "https://discord.com/api/v8/interactions/{0}/{1}/callback".format(id, token)
                json = {
                    "type": 4,
                    "data": {
                        "content": "pogggggggggggggggg"
                    }
                }
                r = requests.post(url, json=json)
