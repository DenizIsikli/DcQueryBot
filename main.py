import discord
from discord.ext import commands
from dataclasses import dataclass
import asyncio
import os
from dotenv import load_dotenv
import install as install


class Setup:
    def __init__(self):
        pass

    @staticmethod
    async def setup_query_instances(bot):
        loaded_queries = []

        try:
            for filename in os.listdir("ApiQueries"):
                if filename.endswith(".py"):
                    query_name = f"ApiQueries.{filename[:-3]}"  # Remove the last 3 characters (.py)
                    try:
                        await bot.load_extension(query_name)
                        loaded_queries.append(query_name)
                    except Exception as e:
                        print(f"Failed to load Cog file: {query_name}: {e}")
        except Exception as e:
            print(f"Failed to load Query files: {e}")

        if loaded_queries:
            for query in loaded_queries:
                print(f"Loaded Query File(s): {query}")
            print("\n")

    @staticmethod
    async def setup_cog_instances(bot):
        loaded_cogs = []

        try:
            for filename in os.listdir("Cogs"):
                if filename.endswith(".py"):
                    cog_name = f"Cogs.{filename[:-3]}"  # Remove the last 3 characters (.py)
                    try:
                        await bot.load_extension(cog_name)
                        loaded_cogs.append(cog_name)
                    except Exception as e:
                        print(f"Failed to load Cog file: {cog_name}: {e}")
        except Exception as e:
            print(f"Failed to load Cog files: {e}")

        if loaded_cogs:
            for cog in loaded_cogs:
                print(f"Loaded Cog File(s): {cog}")
            print("\n")

    @staticmethod
    async def setup_util_instances(bot):
        loaded_utils = []

        try:
            for filename in os.listdir("Utility"):
                if filename.endswith(".py"):
                    util_name = f"Utility.{filename[:-3]}"  # Remove the last 3 characters (.py)
                    try:
                        await bot.load_extension(util_name)
                        loaded_utils.append(util_name)
                    except Exception as e:
                        print(f"Failed to load Util file: {util_name}: {e}")
        except Exception as e:
            print(f"Failed to load Util files: {e}")

        if loaded_utils:
            for util in loaded_utils:
                print(f"Loaded Util File(s): {util}")
            print("\n")


@dataclass
class Intents:
    message_content: bool = True
    guild_messages: bool = True
    dm_messages: bool = True

    def create_instance(self):
        intents = discord.Intents.default()
        intents.message_content = self.message_content
        intents.guild_messages = self.guild_messages
        intents.dm_messages = self.dm_messages
        return intents


# Instance of intents
intents_instance = Intents().create_instance()


class Main:
    def __init__(self):
        self.setup = Setup()
        self.base_dir = "C:/Users/deniz/PycharmProjects/DcQueryBot/config/config.env"
        self.owner_id = 538816980845854720

    async def main(self):
        bot = commands.Bot(command_prefix="!", owner_id=self.owner_id, intents=intents_instance)
        bot.remove_command('help')

        @bot.event
        async def on_ready():
            await bot.change_presence(activity=discord.Game(f"!help"))

            print(f"Logged in as {bot.user}")
            print("_____________________________")

        load_dotenv(dotenv_path=self.base_dir, verbose=True)
        bot_token = os.getenv("BOT_TOKEN")
        setup_instance = self.setup
        await setup_instance.setup_query_instances(bot)
        await setup_instance.setup_cog_instances(bot)
        await setup_instance.setup_util_instances(bot)
        await bot.start(bot_token)


if __name__ == "__main__":
    main_instance = Main()
    asyncio.run(main_instance.main())
