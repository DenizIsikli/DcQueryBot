import re
import random
import aiohttp
import discord
import datetime
from discord.ext import commands


class UrbanDictionaryQuery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.URBAN_DICTIONARY_API = "https://api.urbandictionary.com/v0/define"

    @staticmethod
    def remove_brackets(text):
        # Remove brackets from text
        return re.sub(r'\[([^\]]+)]', r'\1', text)

    async def urban_dictionary_query(self, ctx, word_amount: int = 1, search_query: str = None):
        if ctx.author == ctx.bot.user:
            return

        if search_query is None:
            await ctx.send("Please provide a search query.")
            return

        if word_amount < 1 or word_amount > 5:
            await ctx.send("Word amount must be between 1 and 5.")
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
                        random.shuffle(search_results)

                        search_results_limited = search_results[:word_amount]

                        for i, result in enumerate(search_results_limited):
                            title = result["word"]
                            meaning = self.remove_brackets(result["definition"])
                            example = self.remove_brackets(result["example"])

                            embed = discord.Embed(
                                title=f"**Term {i + 1}/{word_amount}**: {title}",
                                color=discord.Color.blue()
                            )
                            embed.add_field(name="**Meaning**: ", value=meaning, inline=False)
                            embed.add_field(name="**Example(s)**: ", value=example, inline=False)

                            # Add & set footer with timestamp
                            timestamp = datetime.datetime.utcnow()
                            embed.timestamp = timestamp
                            embed.set_footer(text=f"Requested by {ctx.author.name}")

                            await ctx.send(embed=embed)
                    else:
                        return

        except aiohttp.ClientOSError as e:
            await ctx.send(f"An error occurred while querying Urban Dictionary: {e}")

        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    @commands.command()
    async def urban(self, ctx, word_amount=1, *, search_query=None):
        await self.urban_dictionary_query(ctx, word_amount, search_query=search_query)

    @urban.error
    async def urban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `!urban <word_amount> <search_query>`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Please provide a word amount (integer)")
        else:
            await ctx.send(f"An error occurred: {error}")


async def setup(bot):
    await bot.add_cog(UrbanDictionaryQuery(bot))
