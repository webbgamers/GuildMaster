from io import BytesIO
import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def member_allows_impersonations(self, member):
        # Get data for requested user
        user_data = await self.bot.db_client[str(member.guild.id)].user_data.find_one({"_id": str(member.id)})
        # Create new document for user if it doesnt exist
        if user_data is None:
            # Copy default user document and change values to match new user
            default_user = await self.bot.db_client.default_server.user_data.find_one({"_id": "0"})
            default_user["_id"] = str(member.id)
            await self.bot.db_client[str(member.guild.id)].user_data.insert_one(default_user)
            return True
        try:
            return user_data["impersonation"]
        except KeyError:
            return True
        

    @commands.command()
    async def impersonate(self, ctx, member:discord.Member, *, message):
        if not await self.member_allows_impersonations(ctx.message.author):
            await ctx.send("You must allow others to impersonate you to impersonate anyone.")
            return
        elif not await self.member_allows_impersonations(member):
            await ctx.send("{} does not want anyone impersonating them.".format(member.display_name))
            return
        attachment = None
        if ctx.message.attachments != []:
            b = BytesIO()
            attachment = ctx.message.attachments[0]
            ab = await attachment.read()
            b.write(ab)
            b.seek(0)
            attachment = discord.File(b, attachment.filename, spoiler=attachment.is_spoiler())
        await ctx.message.delete()
        webhooks = await ctx.message.guild.webhooks()
        w = None
        for webhook in webhooks:
            if webhook.user.id == self.bot.user.id and webhook.channel.id == ctx.message.channel.id:
                w = webhook
                break
        if w is None:
            w = await ctx.message.channel.create_webhook(name="GM Webhook", reason="Impersonation")
        
        await w.send(message, username=member.display_name, avatar_url=member.avatar_url, file=attachment)
    
    @commands.command(name="noimpersonate")
    async def no_impersonation(self, ctx):
        current_pref = await self.member_allows_impersonations(ctx.message.author)
        await self.bot.db_client[str(ctx.message.guild.id)].user_data.find_one_and_update({"_id": str(ctx.message.author.id)}, {"$set": {"impersonation": not current_pref}})
        if current_pref is True:
            await ctx.send("People in this server will no longer be able to impersonate you. Run this command again to re-enable impersonation.")
        else:
            await ctx.send("People in this server will now be able to impersonate you.")
    
    @commands.command()
    async def echo(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    async def spacify(self, ctx, *, message):
        new_message = ""
        for i in range(0, len(message) - 1):
            new_message += message[i] + " "
        new_message += message[len(message) - 1]
        await ctx.send("`{}`".format(new_message))


def setup(bot):
    print("Loading Fun extension...")
    bot.add_cog(Fun(bot))