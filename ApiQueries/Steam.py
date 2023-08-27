import json
import aiohttp
import discord
from datetime import datetime
from discord.ext import commands


class SteamQuery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.STEAM_API = f"https://steam2.p.rapidapi.com/search/"

    async def steam_query(self, ctx, *, game: str = None):
        if ctx.author == ctx.bot.user:
            return

        if game is None:
            await ctx.send("Please provide the name of a game.")
            return

        endpoint = f"{self.STEAM_API}{game}/page/1"

        try:
            headers = {
                "X-RapidAPI-Key": "2ba10896fdmsh6eb24b198a7b520p1fef74jsneb8afa07df45",
                "X-RapidAPI-Host": "steam2.p.rapidapi.com"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, headers=headers) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_json = await response.json()

                    if not response_json:
                        await ctx.send("No results found for the provided game.")
                        return

                    try:
                        game_info = response_json[0]

                        title = game_info.get('title', 'Title not found')
                        review_summary = game_info.get('reviewSummary', 'Review summary not found')
                        released = game_info.get('released', 'Released not found')
                        url = game_info.get('url', 'Url not found')
                        img_url = game_info.get('imgUrl', 'Image Url not found')

                        review_summary = review_summary.replace("<br>", "\n")

                        embed = discord.Embed(
                            title=f"{title}",
                            description=f"**Review summary**\n{review_summary}",
                            url=url,
                            color=discord.Color.dark_theme()
                        )

                        embed.set_thumbnail(url=img_url)
                        embed.add_field(name="Release:", value=f"{released}")

                        # Add & set footer with timestamp
                        timestamp = datetime.utcnow()
                        embed.timestamp = timestamp
                        embed.set_footer(text=f"Requested by {ctx.author.name}")

                        await ctx.send(embed=embed)

                    except json.JSONDecodeError:
                        await ctx.send("Error decoding JSON response.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def steam(self, ctx, *, game: str = None):
        await self.steam_query(ctx, game=game)


async def setup(bot):
    await bot.add_cog(SteamQuery(bot))

