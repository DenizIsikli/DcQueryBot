import discord
from discord.ext import commands
import DcQuery
import asyncio


class Main:
    @staticmethod
    async def main():
        intents_instance = DcQuery.intents_instance
        bot = commands.Bot(command_prefix="!", intents=intents_instance)

        setup_instance = DcQuery.Setup()
        await setup_instance.setup(bot)

        @bot.event
        async def on_ready():
            await bot.change_presence(activity=discord.Game('!help'))
            print(f"Logged in as {bot.user}")

        return bot  # Return the bot instance


if __name__ == "__main__":
    bot = asyncio.run(Main.main())
    bot_token = "MTEzNjA3MTM5ODk5Mzk2MTEyMg.G3TDmh.cbps9v_FUpdQ6EScMrL7hSJllYuQNpOTeXGmHQ"
    bot.run(bot_token)
