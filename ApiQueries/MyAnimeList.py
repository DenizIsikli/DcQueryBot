import json
import aiohttp
from discord.ext import commands


class MyAnimeList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.MYANIMELIST_API = "https://myanimelist.p.rapidapi.com/anime/search/"

    async def my_anime_list(self, ctx, *, anime: str = None):
        if ctx.author == ctx.bot.user:
            return

        self.anime = anime

        try:
            headers = {
                "X-RapidAPI-Key": "2ba10896fdmsh6eb24b198a7b520p1fef74jsneb8afa07df45",
                "X-RapidAPI-Host": "myanimelist.p.rapidapi.com"
            }

            params = {
                "q": anime
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.MYANIMELIST_API, headers=headers, params=params) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_text = await response.text()
                    response_data = json.loads(response_text)

                    print(response.content_type)
                    print(response_text)

                    if response_data:
                        result = response_data[0]

                        title = result.get('title', 'Title not found')
                        episodes = result.get('num_episodes', 'Episodes not found')
                        aired = result.get('aired', {}).get('from', 'Airing date not found')
                        genres = result.get('genres', [])

                        genre_list = ", ".join(genres) if genres else 'No genres found'

                        await ctx.send(f"```\n"
                                       f"Title: {title}\n"
                                       f"Episodes: {episodes}\n"
                                       f"Aired: {aired}\n"
                                       f"Genres: {genre_list}\n"
                                       f"```")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def anilist(self, ctx, *, anime):
        await self.my_anime_list(ctx, anime=anime)


async def setup(bot):
    await bot.add_cog(MyAnimeList(bot))
