import Secrets
import motor.motor_asyncio
from discord.ext import commands

print("Connecting...")

commandPrefix = "$"
bot = commands.Bot(command_prefix=commandPrefix)
bot.owner_id = 300291449403080704
bot.db_client = motor.motor_asyncio.AsyncIOMotorClient(Secrets.get_db_uri())
bot.RED = 0xff0000
bot.GREEN = 0x00ff00
bot.YELLOW = 0xffff00
print("Connected to MongoDB")

bot.load_extension("Developer")
bot.load_extension("General")
bot.load_extension("Leveling")
bot.load_extension("Information")
bot.load_extension("Fun")
bot.load_extension("Interactions")

bot.run(Secrets.get_token())
