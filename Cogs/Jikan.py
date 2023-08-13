import datetime
import discord
from discord.ext import commands
import aiohttp


class Jikan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.JIKAN_API = "https://api.jikan.moe/v3/anime"

    async def my_anime_list_query(self, bot, message: discord.Message, search_query: str = None):
        if message.author == bot.user:
            return

        try:
            params = {
                "q": search_query
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.JIKAN_API, params=params) as response:
                    if response.status == 410:
                        await message.channel.send("The requested anime is not found.")
                        return

                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_data = await response.json()

                    first_result = response_data.get("results", [])[0]

                    title = first_result.get("title", "N/A")
                    description = first_result.get("synopsis", "N/A")
                    rating = first_result.get("score", "N/A")

                    embed = discord.Embed(
                        title=f"**Title**: {title}",
                        color=discord.Color.magenta()
                    )
                    embed.add_field(name="**Description**: ", value=description, inline=False)
                    embed.add_field(name="**Rating**: ", value=rating, inline=False)

                    # Add & set footer with timestamp
                    timestamp = datetime.datetime.utcnow()
                    embed.timestamp = timestamp
                    embed.set_footer(text=f"Requested by {message.author.name}")

                    await message.channel.send(embed=embed)

        except aiohttp.ClientOSError as e:
            await message.channel.send(f"An error occurred while querying MyAnimeList: {e}")

        except Exception as e:
            await message.channel.send(f"An unexpected error occurred: {e}")

    @commands.command()
    async def jikan(self, ctx, *args):
        # Combine arguments into a single search query
        search_query = " ".join(args)

        if not search_query:
            await ctx.send("Please provide a search query.")
            return

        await self.my_anime_list_query(ctx.bot, ctx.message, search_query)


async def setup(bot):
    await bot.add_cog(Jikan(bot))
