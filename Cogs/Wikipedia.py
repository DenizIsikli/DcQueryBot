from discord.ext import commands
import aiohttp


class WikipediaQuery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

    async def wikipedia_query(self, ctx, limit: int = 1, search_query: str = None):
        if ctx.author == ctx.bot.user:
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

                            await ctx.send(f""
                                           f"**Search Result {i + 1}/{query_limit}**: {title}\n"
                                           f"**Page URL**: {page_url}"
                                           )
                    else:
                        return

        except aiohttp.ClientOSError as e:
            await ctx.send(f"An error occurred while querying Wikipedia: {e}")

        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    @commands.command()
    async def wiki(self, ctx, *args, limit=1, search_query=""):
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

        await self.wikipedia_query(ctx, limit, search_query)

    @wiki.error
    async def wiki_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `!wiki [<limit>] <search_query>`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Please provide a valid limit (integer) and search query.")
        else:
            await ctx.send(f"An error occurred: {error}")


async def setup(bot):
    await bot.add_cog(WikipediaQuery(bot))
