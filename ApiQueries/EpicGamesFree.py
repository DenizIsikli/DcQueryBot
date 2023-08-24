import aiohttp
from discord.ext import commands


class EpicGamesFree(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.EPICGAMES_API = "https://epic-free-games.p.rapidapi.com/epic-free-games"

    async def epic_games_free(self, ctx):
        if ctx.author == ctx.bot.user:
            return

        try:
            headers = {
                "X-RapidAPI-Key": "2ba10896fdmsh6eb24b198a7b520p1fef74jsneb8afa07df45",
                "X-RapidAPI-Host": "epic-free-games.p.rapidapi.com"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.EPICGAMES_API, headers=headers) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_json = await response.json()

                    response_data = response_json[""][0]
                    game_name = response_data["name"]
                    game_description = response_data["description"]
                    game_publisher = response_data["publisher"]
                    game_discount_price = response_data["discountPrice"]
                    game_original_price = response_data["originalPrice"]
                    game_currencyCode = response_data["currencyCode"]
                    game_url = response_data["appUrl"]

                    print(str(game_name))

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def epicgames(self, ctx):
        await self.epic_games_free(ctx)


async def setup(bot):
    await bot.add_cog(EpicGamesFree(bot))
