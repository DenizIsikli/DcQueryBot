import datetime
import discord
from discord.ext import commands
import aiohttp
import main
from dataclasses import dataclass


@dataclass
class Baseclass:
    intents_instance = main.Intents


class UrbanDictionaryQuery(commands.Cog):
    def __init__(self):
        self.URBAN_DICTIONARY_API = "https://api.urbandictionary.com/v0/define"

    async def urban_dictionary_query(self, bot, message: discord.Message, limit: int = 1, search_query: str = None):
        if message.author == bot.user:
            return

        try:
            params = {
                "term": search_query
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.URBAN_DICTIONARY_API, params=params) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_data = await response.json()

            if "list" in response_data:
                search_results = response_data["list"]
                query_limit = limit

                for i, result in enumerate(search_results[:query_limit]):
                    title = result["word"]
                    meaning = result["definition"]
                    example = result["example"]

                    embed = discord.Embed(title=f"**Term {i + 1}/{query_limit}**: {title}", color=discord.Color.blue())
                    embed.add_field(name="**Meaning**: ", value=meaning, inline=False)
                    embed.add_field(name="**Example**: ", value=example, inline=False)

                    # Add & set footer with timestamp
                    timestamp = datetime.datetime.utcnow()
                    embed.timestamp = timestamp
                    embed.set_footer(text=f"Requested by {message.author.name}")

                    await message.channel.send(embed=embed)
            else:
                await message.channel.send("No search results found for the query.")

        except aiohttp.ClientOSError as e:
            await message.channel.send(f"An error occurred while querying Urban Dictionary: {e}")

        except Exception as e:
            await message.channel.send(f"An unexpected error occurred: {e}")

    @commands.command(intents=Baseclass.intents_instance)
    async def urban(self, bot, ctx, *args):
        limit = 1
        search_query = ""

        if args:
            if args[0].isdigit():
                limit = int(args[0])
                search_query = " ".join(args[1:])
            elif args[-1].isdigit():
                pass
        else:
            search_query = " ".join(args)

        await self.urban_dictionary_query(bot, ctx.message, limit, search_query)


async def setup(bot):
    await bot.add_cog(UrbanDictionaryQuery())
