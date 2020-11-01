import Secrets
import motor.motor_asyncio
from discord.ext import commands
from bson import SON

print("Connecting...")

commandPrefix = "$"
bot = commands.Bot(command_prefix=commandPrefix)
bot.owner_id = 300291449403080704
bot.db_client = motor.motor_asyncio.AsyncIOMotorClient(Secrets.get_db_uri())
print("Connected to MongoDB")

bot.load_extension("Leveling")


@bot.event
async def on_ready():
    print("Connected to Discord with ID {}.".format(bot.user.id))


@bot.command()
async def test(ctx):
    await ctx.send("hello!")


@bot.command()
async def dbtest(ctx):
    db_list = await bot.db_client["admin"].command(SON([("listDatabases", 1), ("nameOnly", True)]))
    await ctx.send(db_list)

bot.run(Secrets.get_token())
