import discord
from discord.ext import commands
import requests
import DcQuery


intents_instance = DcQuery.intents_instance


class UrbanDictionaryQuery(commands.Cog):
    def __init__(self):
        self.URBAN_DICTIONARY_API = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
        self.bot = commands.Bot(command_prefix="!", intents=intents_instance)

    async def urban_dictionary_query(self, message: discord.Message, limit: int = 1, search_query: str = None):
        if message.author == self.bot.user:
            return

        try:
            headers = {
                "X-RapidAPI-Host": "mashape-community-urban-dictionary.p.rapidapi.com",
                "X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY_HERE"  # Replace with your actual RapidAPI key
            }

            params = {
                "term": search_query
            }

            response = requests.get(self.URBAN_DICTIONARY_API, headers=headers, params=params)
            response.raise_for_status()  # Raise an exception if the request was not successful

            response_data = response.json()

            if "list" in response_data:
                definitions = response_data["list"]
                query_limit = limit

                for i, definition in enumerate(definitions):
                    title = definition["word"]
                    meaning = definition["definition"]
                    example = definition["example"]

                    await message.channel.send(f""
                                               f"Term {i + 1}/{query_limit}: {title}\n"
                                               f"Meaning: {meaning}\n"
                                               f"Example: {example}\n\n"
                                               )
            else:
                await message.channel.send("No search results found for the query.")

        except requests.RequestException as e:
            await message.channel.send(f"An error occurred while querying Urban Dictionary: {e}")

        except Exception as e:
            await message.channel.send(f"An unexpected error occurred: {e}")

    @commands.command(intents=intents_instance)
    async def urban(self, ctx, *args):
        limit = 1
        search_query = ""

        if args:
            if args[0].isdigit():
                limit = int(args[0])
                search_query = " ".join(args[1:])
            else:
                search_query = " ".join(args)

        await self.urban_dictionary_query(ctx.message, limit, search_query)


class Setup(commands.Cog):
    def __init__(self):
        pass

    @staticmethod
    async def setup(bot):
        await bot.add_cog(UrbanDictionaryQuery())
