import discord
from discord.ext import commands
from dataclasses import dataclass
import asyncio
import os


class Setup:
    def __init__(self):
        pass

    async def setup_cog_instances(self, bot):
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                cog_name = f"Cogs.{filename[:-3]}"  # Remove the last 3 characters (.py)
                try:
                    await bot.load_extension(cog_name)
                    print(f"Loaded Cog File: {cog_name}")
                except Exception as e:
                    print(f"Failed to load cog: {cog_name}: {e}")

        try:
            # Load DcQuery directly
            await bot.load_extension("DcQuery")
            print("Loaded Util File: DcQuery\n")
        except Exception as e:
            print(f"Failed to load DcQuery: {e}")


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
        self.setup_instance = Setup()

    async def main(self):
        bot = commands.Bot(command_prefix="!", owner_id=538816980845854720, intents=intents_instance)
        bot.remove_command('help')

        @bot.event
        async def on_ready():
            await bot.change_presence(activity=discord.Game('!help'))
            print(f"Logged in as {bot.user}")
            print("_____________________________")

        bot_token = "MTEzNjA3MTM5ODk5Mzk2MTEyMg.G3TDmh.cbps9v_FUpdQ6EScMrL7hSJllYuQNpOTeXGmHQ"
        setup_instance = Setup()
        await setup_instance.setup_cog_instances(bot)
        await bot.start(bot_token)


if __name__ == "__main__":
    main_instance = Main()
    asyncio.run(main_instance.main())
