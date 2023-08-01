import os
import discord
import requests
from urllib.parse import quote
from dotenv import load_dotenv

class LoadEnvironmentVariables:
    @staticmethod
    def load_environment_variables():
        load_dotenv()
        return {
            "BOT_TOKEN": os.getenv("BOT_TOKEN")
        }

class BaseClass:
    def __init__(self):
        # Load config settings - mail and password
        env_vars = LoadEnvironmentVariables.load_environment_variables()

        # Discord bot token (replace 'YOUR_BOT_TOKEN' with your actual bot token)
        self.BOT_TOKEN = env_vars["BOT_TOKEN"]
        # Pricerunner base URL
        self.PRICERUNNER_URL = "https://www.pricerunner.dk"
        # Initialize the Discord bot
        self.bot = discord.Client()


class ReadyHandler(BaseClass):
    def __init__(self):
        # Call the BaseClass constructor
        super().__init__()

    async def on_ready(self):
        print(f"Logged in as {self.bot.user}")


class MessageHandler(BaseClass):
    def __init__(self):
        # Call the BaseClass constructor
        super().__init__()

    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith("!search"):
            search_query = message.content[len("!search"):].strip()
            if not search_query:
                await message.channel.send("Please provide a search term after '!search'.")
                return

            # Encode the search query for safe URL usage
            encoded_search_query = quote(search_query)

            # Make a GET request to PriceRunner
            response = requests.get(f"{self.PRICERUNNER_URL}/s?search={encoded_search_query}")

            if response.status_code == 200:
                # Parse the response and get the relevant data
                # (you'll need to inspect the HTML of the Pricerunner page to extract the data)
                # Here, we are just returning the HTML content as a .txt file.
                file_content = response.text
                with open(f"{search_query}_results.txt", "w") as file:
                    file.write(file_content)

                # Send the .txt file back to the user on Discord
                await message.channel.send(file=discord.File(f"{search_query}_results.txt"))
            else:
                await message.channel.send("Error fetching data from Pricerunner.")


class EventHandler(BaseClass):
    def __init__(self):
        # Call the BaseClass constructor
        super().__init__()

    @staticmethod
    def eventhandler():
        ready_handler = ReadyHandler()
        message_handler = MessageHandler()

        ready_handler.bot.run(ready_handler.BOT_TOKEN)
        message_handler.bot.run(message_handler.BOT_TOKEN)
