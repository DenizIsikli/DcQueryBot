import discord
import PriceRunner


class Main:
    @staticmethod
    def main():
        event_handler = PriceRunner

        bot = event_handler.bot
        bot.run(event_handler.BOT_TOKEN)

if __name__ == "__main__":
    Main.main()