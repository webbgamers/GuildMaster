from discord.ext import commands


def filter_message(message_content, blacklist, substitute_numbers=True, sensitive_filtering=False):
    # Some lists of characters
    punctuation_list = [".", ",", ";", ":", "!", "?", "\\", "/", "\n", "+", "=", "-", "@"]
    discord_char_list = ["|", "~", "`", "_", "*", "<", ">"]
    number_letter_translations = [("0", "o"), ("1", "l"), ("3", "e"), ("4", "a"), ("5", "s"), ("9", "g")]

    blacklisted_words = []

    # Remove characters used by discord markdown
    for discord_char in discord_char_list:
        message_content = message_content.replace(discord_char, "")

    # Remove punctuation
    for punctuation in punctuation_list:
        message_content = message_content.replace(punctuation, "")

    # Sensitive filtering
    if sensitive_filtering is True:
        # Remove spaces
        message_content = message_content.replace(" ", "")
        # Substitute letters for numbers
        if substitute_numbers is True:
            for translation in number_letter_translations:
                message_content = message_content.replace(translation[0], translation[1])
        for bad_word in blacklist:
            if bad_word in message_content:
                blacklisted_words.append(bad_word)

    # Normal filtering
    else:
        # Split message into separate words
        word_list = message_content.split(" ")
        # Substitute letters for numbers
        if substitute_numbers is True:
            word_index = 0
            for word in word_list:
                if not word.isdigit():
                    for translation in number_letter_translations:
                        word = word.replace(translation[0], translation[1])
                word_list[word_index] = word
                word_index += 1
        # Check word list for blacklisted words
        for word in word_list:
            if word in blacklist:
                blacklisted_words.append(word)

    return blacklisted_words


class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_message_settings(self, message):
        # Get settings from database
        message_settings = await self.bot.db_client.message_settings[str(message.guild.id)].find_one({"_id": str(message.channel.id)})
        # Create document for channel if it does not exits
        if message_settings is None:
            # Try to get the default settings document for that server
            default_settings = await self.bot.db_client.message_settings[str(message.guild.id)].find_one({"_id": "0"})
            # Create default settings document if it doesnt exist
            if default_settings is None:
                # Copy master default document into server collection
                default_settings = await self.bot.db_client.message_settings.default_server.find_one({"_id": "0"})
                await self.bot.db_client.message_settings[str(message.guild.id)].insert_one(default_settings)
            message_settings = default_settings # line 69 nice
        return message_settings

    async def award_xp(self, xp, message):
        # Add xp to correct user
        original_data = await self.bot.db_client.user_data[str(message.guild.id)].find_one_and_update({"_id": str(message.author.id)}, {"$inc": {"xp": xp}})
        # Create new document for user if it doesnt exist"
        if original_data is None:
            # Copy default user document and change values to match new user
            default_user = await self.bot.db_client.user_data.default_server.find_one({"_id": "0"})
            default_user["_id"] = str(message.author.id)
            default_user["xp"] = xp
            await self.bot.db_client.user_data[str(message.guild.id)].insert_one(default_user)
        print("Awarded {0} xp for message with id {1}.".format(xp, message.id))

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            # Get message settings from database
            message_settings = await self.get_message_settings(message)

            # Check for any blacklisted words and take action accordingly
            filter_settings = message_settings["filter_settings"]
            filter_message(message.content, filter_settings["word_list"])

            # Award xp based on retrieved settings
            xp_settings = message_settings["xp_settings"]
            message_xp = 0
            if xp_settings["mode"] == 1:
                allowed_charset = set(xp_settings["allowed_chars"])
                for char in allowed_charset:
                    message_xp += message.content.count(char)
            elif xp_settings["mode"] == 2:
                message_xp = xp_settings["xp"]
            message_xp *= xp_settings["multiplier"]
            await self.award_xp(message_xp, message)


def setup(bot):
    bot.add_cog(Leveling(bot))
