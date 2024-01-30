import os
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

    @staticmethod
    async def scrape_product_data(item_div):
        name_element = item_div.find('h3', class_='pr-c6rk6p')
        info_element = item_div.find('p', class_='pr-f6mg9h')
        price_element = item_div.find('span', class_='pr-yp1q6p')
        link_element = item_div.find('a')['href']

        # Extract product information in text format within each product's container
        name = name_element.text if name_element else None
        info = info_element.text if info_element else None
        price = price_element.text.replace('\xa0', '') if price_element else None
        link = f"https://www.pricerunner.dk{link_element}" if link_element else None

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

    @staticmethod
    async def run(self, ctx, product_name=None):
        try:
            if product_name is None:
                await ctx.send("Please enter a product name")

            products = await self.search_product(product_name)

            if products:
                for i, product in enumerate(products[:20]):
                    _product_name_ = product.name
                    _product_info_ = product.info
                    _product_price_ = product.price
                    _product_link_ = product.link

                    response_str = f"{i + 1}: {_product_name_}\n{_product_info_}\n{_product_price_}\n{_product_link_}\n"

                # response_str = '\n'.join(f"{i + 1}: {product}\n" for i, product in enumerate(products[:20]))
                print(f"{response_str}\n")

                with open('PriceRunner.txt', 'w') as f:
                    f.write(response_str)

                await ctx.send(file=discord.File('PriceRunner.txt'))
                os.remove(f'PriceRunner{product_name}.txt')

            else:
                await ctx.send("No results found for the provided product.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def pricerunner(self, ctx, *, product_name=None):
        await self.run(self, ctx, product_name)


async def setup(bot):
    await bot.add_cog(PriceRunnerAPI(bot))
