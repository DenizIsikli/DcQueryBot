import json
import aiohttp
import discord
from datetime import datetime
from discord.ext import commands


class MyAnimeList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.MYANIMELIST_API_ANIME = "https://myanimelist.p.rapidapi.com/anime/search/"
        self.MYANIMELIST_API_MANGA = "https://myanimelist.p.rapidapi.com/manga/search/"

    async def my_anime_list_anime(self, ctx, *, anime: str = None):
        if ctx.author == ctx.bot.user:
            return

        if anime is None:
            await ctx.send("Please provide the name of an anime.")
            return

        endpoint = f"{self.MYANIMELIST_API_ANIME}{anime}"

        try:
            headers = {
                "X-RapidAPI-Key": "2ba10896fdmsh6eb24b198a7b520p1fef74jsneb8afa07df45",
                "X-RapidAPI-Host": "myanimelist.p.rapidapi.com"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, headers=headers) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_json = await response.json()

                    if not response_json:
                        await ctx.send("No results found for the provided anime.")
                        return

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
        await self.my_anime_list_anime(ctx, anime=anime)

    async def my_anime_list_manga(self, ctx, *, manga: str = None):
        if ctx.author == ctx.bot.user:
            return

        if manga is None:
            await ctx.send("Please provide the name of a manga.")
            return

        endpoint = f"{self.MYANIMELIST_API_MANGA}{manga}"

        try:
            headers = {
                "X-RapidAPI-Key": "2ba10896fdmsh6eb24b198a7b520p1fef74jsneb8afa07df45",
                "X-RapidAPI-Host": "myanimelist.p.rapidapi.com"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint, headers=headers) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_json = await response.json()

                    if not response_json:
                        await ctx.send("No results found for the provided anime.")
                        return

                    try:
                        manga_info = response_json[0]

                        title = manga_info.get('title', 'Title not found')
                        description = manga_info.get('description', 'Description not found')
                        picture_url = manga_info.get('picture_url', 'Picture URL not found')
                        myanimelist_url = manga_info.get('myanimelist_url', 'MyAnimeList URL not found')

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
    async def manga(self, ctx, *, manga: str = None):
        await self.my_anime_list_manga(ctx, manga=manga)


async def setup(bot):
    await bot.add_cog(MyAnimeList(bot))
