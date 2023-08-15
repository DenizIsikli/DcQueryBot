import datetime
import discord
from discord.ext import commands
import aiohttp
import random


class ImgurQuery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.IMGUR_API = "https://api.imgur.com/3/gallery/search/top"

    async def imgur_query(self, bot, message: discord.Message, search_query: str = None):
        if message.author == bot.user:
            return

        try:
            headers = {
                "Authorization": "Client-ID cd4b84872a053b7"
            }

            params = {
                "q": search_query,
                "q-type": "gif",
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.IMGUR_API, headers=headers, params=params) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_data = await response.json()

                    if "data" in response_data:
                        search_results = response_data["data"]

                        if search_results:
                            random_gif = random.randint(0, len(search_results)//2)
                            result = search_results[random_gif]
                            title = result["title"]
                            gif_url = result["link"]

                            await message.channel.send(f"Title: {title}\n{gif_url}")
                    else:
                        await message.channel.send("No search results found for the query.")

        except aiohttp.ClientOSError as e:
            await message.channel.send(f"An error occurred while querying Imgur: {e}")

        except Exception as e:
            await message.channel.send(f"An unexpected error occurred: {e}")

    @commands.command()
    async def imgur(self, ctx, *args, search_query=""):
        if args:
            # Combine arguments into a single search query
            search_query = " ".join(args)

        await self.imgur_query(ctx.bot, ctx.message, search_query)

    @imgur.error
    async def imgur_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument")


async def setup(bot):
    await bot.add_cog(ImgurQuery(bot))
