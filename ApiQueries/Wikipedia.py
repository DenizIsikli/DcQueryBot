import asyncio
import aiohttp
import random
from discord.ext import commands
from textblob import TextBlob
from newspaper import Article


class WikipediaQuery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

    async def wikipedia_query(self, ctx, article_amount: int = 1, search_query: str = None):
        if ctx.author == ctx.bot.user:
            return

        if search_query is None:
            await ctx.send("Please provide a search query.")
            return

        if article_amount < 1 or article_amount > 5:
            await ctx.send("Article amount must be between 1 and 5.")
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
                        random.shuffle(search_results)

                        search_results_limited = search_results[:article_amount]

                        for i, result in enumerate(search_results_limited):
                            title = result["title"]
                            page_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"

                            await ctx.send(f""
                                           f"**Search Result {i + 1}/{article_amount}**: {title}\n"
                                           f"**Page URL**: {page_url}"
                                           )
                    else:
                        await ctx.send("No results found for the provided search query.")
                        return

        except aiohttp.ClientOSError as e:
            await ctx.send(f"An error occurred while querying Wikipedia: {e}")

        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    @commands.command()
    async def wiki(self, ctx, article_amount=1, *, search_query=None):
        await self.wikipedia_query(ctx, article_amount=article_amount, search_query=search_query)

    @wiki.error
    async def wiki_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `!wiki <article_amount> <search_query>`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Please provide an article amount (integer)")
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
