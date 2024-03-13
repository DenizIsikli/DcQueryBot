import os
import time
import discord
from discord.ext import commands
from bs4 import BeautifulSoup
from dataclasses import dataclass
import aiohttp


@dataclass
class Product:
    name: str = None
    price: int = None
    link: str = None


class GGDeals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = "https://gg.deals"
        self.products = []

    async def scrape_product_data(self, item_div):
        name_element = item_div.find('div', class_='game-info-title-wrapper').find('a')['title']
        price_element = item_div.find('span', class_='price-inner game-price-current')
        link_element = item_div.find('a', class_='full-link')['href']

        name = name_element.text if name_element else None
        price = price_element.text.replace('\xa0', '') if price_element else None
        link = f"{self.url}{link_element}" if link_element else None

        return Product(name, price, link)

    async def search_product(self, product_name):
        self.products = [[], []]
        search_url = f'{self.url}/game/?q={product_name.replace("-", "+")}'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(search_url) as response:
                    response.raise_for_status()
                    response_data = await response.text()
                    soup = BeautifulSoup(response_data, 'html.parser')
                    product_div = soup.find('div', class_='col-left')

                    # Official Stores
                    if product_div:
                        for item_div in product_div.find_all('div', id='official-stores'):
                            product = await self.scrape_product_data(item_div)
                            self.products[0].append(product)

                    # Keyshops
                    if product_div:
                        for item_div in product_div.find_all('div', id='keyshops'):
                            product = await self.scrape_product_data(item_div)
                            self.products[1].append(product)

            except aiohttp.ClientError as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

        return self.products

    async def run(self, ctx, product_name=None):
        try:
            output_file = f'GGDeals_{product_name}_{int(time.time())}.txt'

            if product_name is None:
                await ctx.send("Please provide a product name.")
                return

            products = await self.search_product(product_name)
            official_stores = products[0]
            keyshops = products[1]

            if products:
                with open(output_file, 'w') as f:
                    f.write("Official Stores:\n")
                    for i, product in enumerate(official_stores[:10]):
                        product_str = (f"Product {i + 1}:\n"
                                       f"{product.name}\n"
                                       f"{product.price}\n"
                                       f"{product.link}\n")
                        f.write(product_str)

                    f.write("\n\nKeyshops:\n")
                    for i, product in enumerate(keyshops[:10]):
                        product_str = (f"Product {i + 1}:\n"
                                       f"{product.name}\n"
                                       f"{product.price}\n"
                                       f"{product.link}\n")
                        f.write(product_str)

                await ctx.send(file=discord.File(output_file))
                os.remove(output_file)
            else:
                await ctx.send("No results found for the provided product.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def ggdeals(self, ctx, *, product_name=None):
        await self.run(ctx, product_name)

    @ggdeals.error
    async def ggdeals_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `!ggdeals <product_name>`")
        else:
            await ctx.send(f"An error occurred: {error}")


async def setup(bot):
    await bot.add_cog(GGDeals(bot))
