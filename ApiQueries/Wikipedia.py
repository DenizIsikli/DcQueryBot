import asyncio
import aiohttp
from discord.ext import commands
from textblob import TextBlob
from newspaper import Article


class WikipediaQuery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

    async def wikipedia_query(self, ctx, limit: int = 1, search_query: str = None):
        if ctx.author == ctx.bot.user:
            return

        if limit < 0:
            raise commands.BadArgument("Limit cannot be a negative value.")
        elif limit < 1:
            raise commands.BadArgument("Limit must be greater than or equal to 1.")
        elif limit > 5:
            raise commands.BadArgument("Limit must be less than or equal to 5.")

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

                        for i, result in enumerate(search_results[:limit]):
                            title = result["title"]
                            page_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"

                            await ctx.send(f""
                                           f"**Search Result {i + 1}/{limit}**: {title}\n"
                                           f"**Page URL**: {page_url}"
                                           )
                    else:
                        return

        except aiohttp.ClientOSError as e:
            await ctx.send(f"An error occurred while querying Wikipedia: {e}")

        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    @commands.command()
    async def wiki(self, ctx, limit=1, *, search_query=""):
        if limit < 1 or limit > 5:
            await ctx.send("Limit must be between 1 and 5.")
            return

        await self.wikipedia_query(ctx, limit, search_query)

    @wiki.error
    async def wiki_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `!wiki [<limit>] <search_query>`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Please provide a valid limit (integer) and search query.")
        else:
            await ctx.send(f"An error occurred: {error}")


class SentimentAnalysis(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def sentiment_analysis(ctx, link: str = None):
        article = Article(link)

        article.download()
        article.parse()
        article.nlp()

        text = article.summary

        blob = TextBlob(text)

        sentiment = blob.sentiment.polarity

        await ctx.message.delete()
        await asyncio.sleep(0.2)
        await ctx.send(f"Sentiment value: {sentiment}```{link}```")

    @commands.command()
    async def senti(self, ctx, link: str = None):
        await self.sentiment_analysis(ctx, link=link)

    @senti.error
    async def senti_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `!senti <link>`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Please provide a valid link.")
        else:
            await ctx.send(f"An error occurred: {error}")


async def setup(bot):
    await bot.add_cog(WikipediaQuery(bot))
    await bot.add_cog(SentimentAnalysis(bot))
