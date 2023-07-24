import discord
import requests
from urllib.parse import quote

class BaseClass:
    def __init__(self):
        # Discord bot token (replace 'YOUR_BOT_TOKEN' with your actual bot token)
        self.BOT_TOKEN = ""
        # Pricerunner base URL
        self.PRICERUNNER_URL = "https://www.pricerunner.dk"
        # Initialize the Discord bot
        self.bot = discord.Client()

class active:
