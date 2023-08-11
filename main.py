import discord
from discord.ext import commands
import DcQuery
import asyncio
import os


class Main:
    def __init__(self):
        pass

    @staticmethod
    async def setup_all_instances(bot):
        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                cog_name = f"Cogs.{filename}"
                try:
                    bot.load_extension(cog_name)
                    print(f"Loaded cog: {cog_name}")
                except Exception as e:
                    print(f"Failed to load cog: {cog_name}: {e}")

        try:
            # Load DcQuery directly
            bot.load_extension("DcQuery")
            print("Loaded DcQuery")
        except Exception as e:
            print(f"Failed to load DcQuery: {e}")

    async def main(self):
        intents_instance = DcQuery.intents_instance
        bot = commands.Bot(command_prefix="!", owner_id=538816980845854720, intents=intents_instance)

        @bot.event
        async def on_ready():
            await bot.change_presence(activity=discord.Game('!help'))
            print(f"Logged in as {bot.user}")
            print("_____________________________")

        bot_token = "MTEzNjA3MTM5ODk5Mzk2MTEyMg.G3TDmh.cbps9v_FUpdQ6EScMrL7hSJllYuQNpOTeXGmHQ"
        await self.setup_all_instances(bot)
        await bot.start(bot_token)


if __name__ == "__main__":
    main_instance = Main()
    asyncio.run(main_instance.main())
