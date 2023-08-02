import asyncio
import PriceRunner
import discord


class Main:
    @staticmethod
    async def main():
        event_handler = PriceRunner.EventHandler()
        bot = event_handler.bot

        try:
            await bot.start(event_handler.BOT_TOKEN)
        except KeyboardInterrupt:
            await bot.logout()

if __name__ == "__main__":
    asyncio.run(Main.main())
