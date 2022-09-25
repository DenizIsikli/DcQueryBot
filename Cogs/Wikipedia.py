import discord
from discord.ext import commands
import aiohttp


class WikipediaQuery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

    async def wikipedia_query(self, bot, message: discord.Message, limit: int = 1, search_query: str = None):
        if message.author == bot.user:
            return

        try:
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": search_query,
                "utf8": 1
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.WIKIPEDIA_API, params=params) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_data = await response.json()

                    if "query" in response_data and "search" in response_data["query"]:
                        search_results = response_data["query"]["search"]
                        query_limit = limit  # Limit the number of search results to display

                        for i, result in enumerate(search_results[:query_limit]):
                            title = result["title"]
                            page_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"

                            await message.channel.send(f""
                                                       f"**Search Result {i + 1}/{query_limit}**: {title}\n"
                                                       f"**Page URL**: {page_url}"
                                                       )
                    else:
                        await message.channel.send("No search results found for the query.")

        except aiohttp.ClientOSError as e:
            await message.channel.send(f"An error occurred while querying Wikipedia: {e}")

        except Exception as e:
            await message.channel.send(f"An unexpected error occurred: {e}")

    @commands.command()
    async def wiki(self, ctx, *args, limit=1, search_query=""):
        if args:
            if args[0].isdigit():
                limit = int(args[0])
                search_query = " ".join(args[1:])
            elif args[-1].isdigit():
                pass
            else:
                # Combine arguments into a single search query
                search_query = " ".join(args)

        await self.wikipedia_query(ctx.bot, ctx.message, limit, search_query)


async def setup(bot):
    await bot.add_cog(WikipediaQuery(bot))
