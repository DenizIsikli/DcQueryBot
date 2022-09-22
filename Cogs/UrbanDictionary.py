import datetime
import discord
from discord.ext import commands
import aiohttp


class UrbanDictionaryQuery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.URBAN_DICTIONARY_API = "https://api.urbandictionary.com/v0/define"

    async def urban_dictionary_query(self, ctx, limit: int = 1, search_query: str = None):
        if ctx.author == ctx.bot.user:
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

                            embed = discord.Embed(
                                title=f"**Term {i + 1}/{query_limit}**: {title}",
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
    async def urban(self, ctx, *args, limit=1, search_query=""):
        if args:
            if args[0].isdigit():
                limit = int(args[0])
                search_query = " ".join(args[1:])
            elif args[-1].isdigit():
                await ctx.send("The last argument should not be a number!")
                pass
            else:
                # Combine arguments into a single search query
                search_query = " ".join(args)

        await self.urban_dictionary_query(ctx, limit, search_query)

    @urban.error
    async def urban_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument")


async def setup(bot):
    await bot.add_cog(UrbanDictionaryQuery(bot))
