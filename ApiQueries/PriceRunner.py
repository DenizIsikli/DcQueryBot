from discord.ext import commands
import discord
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


@dataclass
class Product:
    name: str = None
    info: str = None
    price: int = None
    link: str = None


class PriceRunnerAPI:
    def __init__(self):
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

        try:
            response = requests.get(search_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                product_div = soup.find('div', class_='mIkxpLfxgo pr-1dtdlzd')

                if product_div:
                    for item_div in product_div.find_all('div', class_='pr-1k8dg1g'):
                        product = self.scrape_product_data(item_div)
                        self.products.append(Product(product.name, product.info, product.price, product.link))

                if soup.find('button', class_='pr-5cnc2s'):
                    pass

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        return self.products

    @staticmethod
    async def run(self, ctx, product_name=None):
        try:
            if product_name is None:
                return ctx.send("Please enter a product name")

            products = self.search_product(product_name)

            if products:
                response_str = '\n'.join(f"{i + 1}: {product}" for i, product in enumerate(products))
                print(f"{response_str}\n")
                ctx.send(response_str)
            else:
                ctx.send("No results found for the provided product.")

        except Exception as e:
            ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def pricerunner(self, ctx, *, product_name=None):
        await self.run(self, ctx, product_name)


async def setup(bot):
    bot.add_cog(PriceRunnerAPI(bot))
