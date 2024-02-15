import discord
from discord.ext import commands
from dataclasses import dataclass
import asyncio
import os
from dotenv import load_dotenv
from setup import Setup


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
        self.base_dir = "config/config.env"
        load_dotenv(self.base_dir, verbose=True)
        self.setup = Setup()
        self.bot_token = os.getenv("BOT_TOKEN")
        self.owner_id = os.getenv("OWNER_ID")

    async def main(self):
        bot = commands.Bot(command_prefix="!", owner_id=int(self.owner_id), intents=intents_instance)
        bot.remove_command('help')

        @bot.event
        async def on_ready():
            await bot.change_presence(activity=discord.Game(f"!help"))

            print(f"Logged in as {bot.user}")
            print("_____________________________")

        await self.setup.setup_instances(bot, "ApiQueries", "Query")
        await self.setup.setup_instances(bot, "Cogs", "Cog")
        await self.setup.setup_instances(bot, "Webscraping", "Crawler")
        await self.setup.setup_instances(bot, "Utility", "Util")

        await bot.start(self.bot_token)


if __name__ == "__main__":
    main_instance = Main()
    asyncio.run(main_instance.main())
