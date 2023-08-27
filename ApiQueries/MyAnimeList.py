import json
import aiohttp
import discord
from datetime import datetime
from discord.ext import commands


class MyAnimeList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.MYANIMELIST_API = "https://myanimelist.p.rapidapi.com/anime/search/"

    async def my_anime_list(self, ctx, *, anime: str = None):
        if ctx.author == ctx.bot.user:
            return

        if anime is None:
            print("hi im here")
            await ctx.send("Please provide the name of an anime.")
            return

        endpoint = f"{self.MYANIMELIST_API}{anime}"

        try:
            headers = {
                "X-RapidAPI-Key": "2ba10896fdmsh6eb24b198a7b520p1fef74jsneb8afa07df45",
                "X-RapidAPI-Host": "myanimelist.p.rapidapi.com"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, headers=headers) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_json = await response.json()

                    try:
                        anime_info = response_json[0]

                        title = anime_info.get('title', 'Title not found')
                        description = anime_info.get('description', 'Description not found')
                        picture_url = anime_info.get('picture_url', 'Picture URL not found')
                        myanimelist_url = anime_info.get('myanimelist_url', 'MyAnimeList URL not found')

                        embed = discord.Embed(
                            title=f"{title}",
                            description=description,
                            url=myanimelist_url,
                            color=discord.Color.dark_theme()
                        )

                        embed.set_thumbnail(url=picture_url)

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
    async def anime(self, ctx, *, anime: str = None):
        await self.my_anime_list(ctx, anime=anime)


async def setup(bot):
    await bot.add_cog(MyAnimeList(bot))
