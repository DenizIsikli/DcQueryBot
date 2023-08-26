import os
import json
import aiohttp
import discord
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
                    response_text = await response.text()
                    response_data = json.loads(response_text)

                    filename = "EpicGamesFreeGames.txt"

                    with open(filename, "w") as file:
                        for game in response_data[:5]:
                            game_name = game["name"]
                            game_description = game["description"]
                            game_publisher = game["publisher"]
                            game_discount_price = game["discountPrice"]
                            game_original_price = game["originalPrice"]
                            game_currency_code = game["currencyCode"]
                            game_url = game["appUrl"]

                            file.write(f"Name: {game_name}\n"
                                       f"Description: {game_description}\n"
                                       f"Publisher: {game_publisher}\n"
                                       f"Discount price: {game_discount_price}\n"
                                       f"Original price: {game_original_price}\n"
                                       f"Currency code: {game_currency_code}\n"
                                       f"URL: {game_url}\n"
                                       f"\n\n\n")

                    await ctx.send(file=discord.File(filename))
                    os.remove(filename)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def epic(self, ctx):
        await self.epic_games_free(ctx)


async def setup(bot):
    await bot.add_cog(EpicGamesFree(bot))
