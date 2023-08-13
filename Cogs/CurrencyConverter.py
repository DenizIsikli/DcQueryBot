import datetime
import discord
import mal
from discord.ext import commands
import aiohttp


class CurrencyConverter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.JIKAN_API = "https://api.apilayer.com/exchangerates_data/latest"

    async def convert_currency(self, bot, message: discord.Message, base_currency: str, target_currency: str, amount: float):
        if message.author == bot.user:
            return

        try:
            params = {
                "q": base_currency
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.JIKAN_API, params=params) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_data = await response.json()

                    conversion_rate = response_data["rates"].get(target_currency)

                    if conversion_rate is None:
                        await message.channel.send(f"Currency '{target_currency}' not found.")
                        return

                    converted_amount = amount * conversion_rate

                    embed = discord.Embed(
                        title="Currency Conversion",
                        description=f"Converted {amount} {base_currency} to {converted_amount:.2f} {target_currency}",
                        color=discord.Color.magenta()
                    )

                    # Add & set footer with timestamp
                    timestamp = datetime.datetime.utcnow()
                    embed.timestamp = timestamp
                    embed.set_footer(text=f"Requested by {message.author.name}")

                    await message.channel.send(embed=embed)

        except Exception as e:
            await message.channel.send(f"An unexpected error occurred: {e}")

    @commands.command()
    async def convert(self, ctx, base_currency: str, target_currency: str, amount: float):
        await self.convert_currency(ctx.message, base_currency, target_currency, amount)


async def setup(bot):
    await bot.add_cog(CurrencyConverter(bot))
