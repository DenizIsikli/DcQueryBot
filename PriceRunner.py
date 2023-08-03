import discord
from discord.ext import commands
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup

# Discord bot token (replace 'YOUR_BOT_TOKEN' with your actual bot token)
BOT_TOKEN = "MTEzNjA3MTM5ODk5Mzk2MTEyMg.G3TDmh.cbps9v_FUpdQ6EScMrL7hSJllYuQNpOTeXGmHQ"
# Pricerunner base URL
PRICERUNNER_URL = "https://www.proshop.dk/"

# Intents for the bot to receive events (specify intents according to your needs)
intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.dm_messages = True

# Initialize the Discord bot as a commands.Bot instance
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message: discord.Message):
    print("Received a message:", message.content)
    if message.author == bot.user:
        return

    if message.content.startswith("!search"):
        search_query = message.content[len("!search"):].strip()
        if not search_query:
            await message.channel.send("Please provide a search term after '!search'.")
            return

        # Encode the search query for safe URL usage
        encoded_search_query = quote(search_query)

        # Make a GET request to PriceRunner
        search_url = f"https://www.proshop.dk/?Search={encoded_search_query}"
        response = requests.get(search_url)

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        product_list = soup.find_all("div", class_="site__product")

        if product_list:
            # Extract product information
            product_info = []
            for product in product_list:
                # name = product.find("a", class_="site-header-link").text.strip()
                current_price = product.find("span", class_="site-currency-lg").text.strip()
                old_price = product.find("div", class_="site-currency-pre").text.strip()
                specs = product.find("div", class_="site-product-link").text.strip()

                # Append the information
                product_info.append(f"Product Name: \n"
                                    f"Current price: {current_price}\n"
                                    f"Old price: {old_price}\n"
                                    f"Specs: {specs}\n")

            # Send the product information back to the user on Discord
            await message.channel.send("\n\n".join(product_info))
            print("made it")
        else:
            await message.channel.send("No products found for the search term.")
            print("Didn't make it")


@bot.command()
async def delete(ctx, message: discord.Message, amount=1):

    if message.author.name == "Denzo":
        try:
            amount = int(amount)
            if amount <= 0:
                await message.channel.send("Please specify a positive number of messages to delete.")
                return

            # Delete the requested number of messages, including the command message
            await message.channel.purge(limit=amount + 1)

        except ValueError:
            await message.channel.send("Please specify a valid number of messages to delete.")
    else:
        await message.channel.send("You don't have permission to delete messages in this channel.")
