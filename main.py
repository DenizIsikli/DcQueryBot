import discord
from discord.ext import commands
import DcQuery
import Features.Wikipedia
import Features.UrbanDictionary
import asyncio


class Main:
    def __init__(self):
        self.setup_instance_misc = DcQuery.Setup()
        self.setup_instance_wikipedia = Features.Wikipedia.Setup()
        self.setup_instance_urban_dictionary = Features.UrbanDictionary.Setup()

    async def setup_all_instances(self, bot):
        setup_instances = [
            self.setup_instance_misc,
            self.setup_instance_wikipedia,
            self.setup_instance_urban_dictionary
        ]

        for instance in setup_instances:
            await instance.setup(bot)

    async def main(self):
        intents_instance = DcQuery.intents_instance
        bot = commands.Bot(command_prefix="!", intents=intents_instance)

        @bot.event
        async def on_ready():
            await bot.change_presence(activity=discord.Game('!help'))
            print(f"Logged in as {bot.user}")

        bot_token = "MTEzNjA3MTM5ODk5Mzk2MTEyMg.G3TDmh.cbps9v_FUpdQ6EScMrL7hSJllYuQNpOTeXGmHQ"
        await self.setup_all_instances(bot)
        await bot.start(bot_token)


if __name__ == "__main__":
    main_instance = Main()
    asyncio.run(main_instance.main())
