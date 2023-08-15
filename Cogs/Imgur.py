import datetime
import discord
from discord.ext import commands
import aiohttp


class ImgurQuery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.IMGUR_API = "https://api.imgur.com/3/gallery/search/top"

    async def imgur_query(self, bot, message: discord.Message, limit: int = 1, search_query: str = None):
        if message.author == bot.user:
            return

        try:
            headers = {
                "Authorization": "cd4b84872a053b7"
            }

            params = {
                "q": search_query,
                "q-type": "gif",
                "limit": limit
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.IMGUR_API, headers=headers, params=params) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_data = await response.json()

                    if "data" in response_data:
                        search_results = response_data["data"]

                        for i, result in enumerate(search_results):
                            title = result["title"]
                            gif_url = result["link"]

                            embed = discord.Embed(
                                title=f"**GIF {i + 1}/{limit}**: {title}",
                                color=discord.Color.red()
                            )
                            embed.set_image(url=gif_url)

                            # Add & set footer with timestamp
                            timestamp = datetime.datetime.utcnow()
                            embed.timestamp = timestamp
                            embed.set_footer(text=f"Requested by {message.author.name}")

                            await message.channel.send(embed=embed)
                    else:
                        await message.channel.send("No search results found for the query.")

        except aiohttp.ClientOSError as e:
            await message.channel.send(f"An error occurred while querying Imgur: {e}")

        except Exception as e:
            await message.channel.send(f"An unexpected error occurred: {e}")

    @commands.command()
    async def imgur(self, ctx, *args, limit=1, search_query=""):
        if args:
            if args[0].isdigit():
                limit = int(args[0])
                search_query = " ".join(args[1:])
            elif args[-1].isdigit():
                pass
            else:
                # Combine arguments into a single search query
                search_query = " ".join(args)

        await self.imgur_query(ctx.bot, ctx.message, limit, search_query)

    @imgur.error
    async def imgur_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument")


async def setup(bot):
    await bot.add_cog(ImgurQuery(bot))
