from discord.ext import commands
import discord
from bson import SON
from discord.gateway import DiscordClientWebSocketResponse



class TestError(Exception):
    """Test exception to test error handling. Can be ignored."""
    pass


class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Connected to Discord with ID {}.".format(self.bot.user.id))
        print("~~~~~~~~~~~~~~~~~~~~~GM~Logs~~~~~~~~~~~~~~~~~~~~~")

    @commands.is_owner()
    @commands.command(name="reload")
    async def reload_extensions(self, ctx):
        embed = discord.Embed(title="Reloading...", color=self.bot.YELLOW)
        embed.set_footer(text="Please wait.")
        message = await ctx.send(embed=embed)
        print("Reloading...")
        self.bot.reload_extension("Developer")
        self.bot.reload_extension("General")
        self.bot.reload_extension("Leveling")
        self.bot.reload_extension("Information")
        success_embed = discord.Embed(title="Success!", color=self.bot.GREEN)
        success_embed.set_footer(text="GuildMaster reloaded by {}.".format(ctx.message.author))
        await message.edit(embed=success_embed)
        print("Reloaded!")
    
    @commands.is_owner()
    @commands.command()
    async def shutdown(self, ctx):
        print("Shutdown initiated from user \"{}\"".format(ctx.message.author))
        await self.bot.logout()

    @commands.command()
    async def dbtest(self, ctx):
        db_list = await self.bot.db_client["admin"].command(SON([("listDatabases", 1), ("nameOnly", True)]))
        await ctx.send(db_list)

    @commands.command()
    async def error(self, ctx):
        raise TestError

    @commands.is_owner()
    @commands.command()
    async def eval(self, ctx, *, command):
        await ctx.send("haha if only")

    @commands.command()
    async def token(self, ctx):
        await ctx.send("NzY5NzI0MjM0MzkyOTI4Mjc3.X5TLjg.dKHDuWCwbKG_R3-RYT-HvKa17IE")

    @commands.command()
    async def embedtest(self, ctx):
        embed = discord.Embed(title="Test Embed", color=self.bot.GREEN)
        embed.add_field(name="Normal Field", value="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.", inline=False)
        embed.add_field(name="Inline Field One", value="Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.", inline=True)
        embed.add_field(name="Inline Field Two", value="Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", inline=True)
        embed.set_footer(text="Requested by {}.".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    print("Loading Developer extension...")
    bot.add_cog(Developer(bot))