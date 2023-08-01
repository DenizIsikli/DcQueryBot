import discord
from discord.ext import commands
import requests


class Intents:
    @staticmethod
    def create_intents():
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guild_messages = True
        intents.dm_messages = True
        return intents


intents_instance = Intents.create_intents()


class WikipediaQuery(commands.Cog):
    def __init__(self):
        self.WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"
        self.bot = commands.Bot(command_prefix="!", intents=intents_instance)

    async def wikipedia_query(self, message: discord.Message, limit: int = 1, search_query: str = None):
        if message.author == self.bot.user:
            return

        try:
            params = {
                "action": "query",
                "format": "json",
                "list": "search",
                "srsearch": search_query,
                "utf8": 1
            }

            response = requests.get(self.WIKIPEDIA_API, params=params)
            response.raise_for_status()  # Raise an exception if the request was not successful

            response_data = response.json()

            if "query" in response_data and "search" in response_data["query"]:
                search_results = response_data["query"]["search"]
                page_limit = limit  # Limit the number of search results to display
                for i, result in enumerate(search_results[:page_limit]):
                    title = result["title"]
                    page_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"

                    await message.channel.send(f""
                                               f"Search Result {i + 1}/{page_limit}: {title}\n"
                                               f"Page URL: {page_url}\n\n"
                                               )
                return
            else:
                await message.channel.send("No search results found for the query.")

        except requests.RequestException as e:
            await message.channel.send(f"An error occurred while querying Wikipedia: {e}")

        except Exception as e:
            await message.channel.send(f"An unexpected error occurred: {e}")

    @commands.command(intents=intents_instance)
    async def wiki(self, ctx, *args):
        limit = 1
        search_query = ""

        if args:
            if args[0].isdigit():
                limit = int(args[0])
                search_query = " ".join(args[1:])
            else:
                search_query = " ".join(args)

        await self.wikipedia_query(ctx.message, limit, search_query)


class AdminDelete(commands.Cog):
    @commands.command(intents=intents_instance)
    async def delete(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)


class Setup(commands.Cog):
    def __init__(self):
        pass

    @staticmethod
    async def setup(bot):
        await bot.add_cog(WikipediaQuery())
        await bot.add_cog(AdminDelete())
