import os
import time
from discord.ext import commands
from bs4 import BeautifulSoup
from dataclasses import dataclass
import aiohttp
import discord


@dataclass
class Product:
    name: str = None
    info: str = None
    price: int = None
    link: str = None


class PriceRunnerAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = "https://www.pricerunner.dk"
        self.products = []

    async def scrape_product_data(self, item_div):
        name_element = item_div.find('h3', class_='pr-c6rk6p')
        info_element = item_div.find('p', class_='pr-f6mg9h')
        price_element = item_div.find('span', class_='pr-yp1q6p')
        link_element = item_div.find('a')['href']

        # Extract product information in text format within each product's container
        name = name_element.text if name_element else None
        info = info_element.text if info_element else None
        price = price_element.text.replace('\xa0', '') if price_element else None
        link = f"{self.url}{link_element}" if link_element else None

        return Product(name, info, price, link)

    async def search_product(self, product_name):
        self.products = []
        search_url = f'{self.url}/search?q={product_name.replace(" ", "+")}'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(search_url) as response:
                    if response.status == 200:
                        text = await response.text()
                        soup = BeautifulSoup(text, 'html.parser')
                        product_div = soup.find('div', class_='mIkxpLfxgo pr-1dtdlzd')

                        if product_div:
                            for item_div in product_div.find_all('div', class_='pr-1k8dg1g'):
                                product = await self.scrape_product_data(item_div)
                                self.products.append(product)

                    if soup.find('button', class_='pr-5cnc2s'):
                        pass

            except aiohttp.ClientError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

        return self.products

    async def run(self, ctx, product_name=None):
        try:
            output_file = f'PriceRunner_{product_name}_{int(time.time())}.txt'

            if product_name is None:
                await ctx.send("Please enter a product name")
                return

            products = await self.search_product(product_name)

            if products:
                with open(output_file, 'w') as f:
                    for i, product in enumerate(products[:20]):
                        product_str = (f"Product {i + 1}:\n"
                                       f"{product.name}\n"
                                       f"{product.info}\n"
                                       f"{product.price}\n"
                                       f"{product.link}\n")
                        f.write(f"{product_str}\n")

                await ctx.send(file=discord.File(output_file))
                os.remove(output_file)
            else:
                await ctx.send("No results found for the provided product.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def pricerunner(self, ctx, *, product_name=None):
        await self.run(ctx, product_name)

    @pricerunner.error
    async def pricerunner_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `!pricerunner <product_name>`")
        else:
            await ctx.send(f"An error occurred: {error}")


async def setup(bot):
    await bot.add_cog(PriceRunnerAPI(bot))
