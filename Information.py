from discord.ext import commands
import discord
import sys
from io import StringIO
import json
from bson import SON
from datetime import date


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def privacy(self, ctx):
        embed = discord.Embed(title="Your data and GuildMaster", color=self.bot.GREEN)
        embed.add_field(name="What is stored?", value="GuildMaster does not store any personal information about you. Your Discord ID which is created by Discord and is available to anyone is stored in order to identify you. GuildMaster also stores several values such as your XP in each server. Information such as the latest command you used will also be stored in order for features such as command cooldowns but they are only stored temporarily. Messages are not logged, however errors that may could contain your ID may be stored to improve the functionality of GuildMaster.", inline=False)
        embed.add_field(name="Who sees your data?", value="GuildMaster does not share your data with any third parties. Developers may see your data while working on the bot or database, but it will not be shared.", inline=False)
        embed.add_field(name="Can you not store my data?", value="If you would not like GuildMaster to store your data, you can use the [coming soon] command. Your ID will still be stored in a blacklist and many commands will have limited functionality.", inline=False)
        embed.add_field(name="Can I see my data?", value="You can request the data that Guildmaster has stored about you with the `datadump` command. This will gather all the data that is linked to you via your Discord ID.", inline=False)
        embed.set_footer(text="Requested by {}.".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(title="GuildMaster Info")
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="Credits", value="webbgamers#0246 - Developer\ndiscord.py - API Wrapper", inline=False)
        embed.add_field(name="Python Version", value="{0}.{1}.{2}".format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
        embed.add_field(name="Discord.py Version", value="{0}.{1}.{2}".format(discord.version_info.major, discord.version_info.minor, discord.version_info.micro))
        embed.add_field(name="Source Code", value="GuildMasters source is currently unavailable but will be soon ;).", inline=False)
        embed.add_field(name="Invite Link", value="Since GuildMaster is still early in development there is currently no way to add it to your server.")
        embed.set_footer(text="Requested by {}.".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def datadump(self, ctx):
        embed1 = discord.Embed(title="Collecting your data...", description="GuildMaster is collecting your data, you should recieve a DM shortly.", color=self.bot.YELLOW)
        embed1.set_footer(text="Requested by {}.".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
        message = await ctx.send(embed=embed1)
        related_documents = {}
        db_list = await self.bot.db_client["admin"].command(SON([("listDatabases", 1), ("nameOnly", True)]))
        for db in db_list["databases"]:
            if db["name"].isdigit():
                document = await self.bot.db_client[db["name"]].user_data.find_one({"_id": str(ctx.author.id)})
                if document is not None:
                    related_documents[db["name"]] = document
        return_document = {"blacklisted": False, "server_data": related_documents}
        file = StringIO()
        file.write(json.dumps(return_document, indent=4))
        file.seek(0)
        current_date = date.today()
        discord_file = discord.File(file, filename="GuildMaster_Data_{0}_{1}_{2}.json".format(current_date.year, current_date.month, current_date.day))
        await ctx.author.send("Here is the data you requested!", file=discord_file)
        embed2 = discord.Embed(title="Data sent!", description="Your data should be in your DMs.", color=self.bot.GREEN)
        embed2.set_footer(text="Requested by {}.".format(ctx.message.author), icon_url=ctx.message.author.avatar_url)
        await message.edit(embed=embed2)

                

def setup(bot):
    print("Loading Information extension...")
    bot.add_cog(Information(bot))
