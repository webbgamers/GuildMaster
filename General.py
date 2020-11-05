import discord
from discord.ext import commands
import time


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        before = time.monotonic()
        embed1 = discord.Embed(title="Pinging...", color=self.bot.YELLOW)
        message = await ctx.send(embed=embed1)
        ping = round((time.monotonic() - before) * 1000, 6)
        embed2 = discord.Embed(title=":ping_pong: Pong!", color=self.bot.GREEN)
        embed2.set_footer(text="{}ms - Requested by {}.".format(ping, ctx.message.author), icon_url=ctx.message.author.avatar_url)
        await message.edit(embed=embed2)

    @commands.command()
    async def suggest(self, ctx, *, feedback):
        await ctx.send("Thank you, your suggestion \"{}\" has not been recorded. Your feedback is not appreciated.".format(feedback))


def setup(bot):
    print("Loading General extension...")
    bot.add_cog(General(bot))