import os
from discord.ext import commands
from bs4 import BeautifulSoup
from dataclasses import dataclass
import aiohttp
import discord

import scrapy
from scrapy import signals
from dataclasses import dataclass


@dataclass
class Product:
    name: str = None
    info: str = None
    price: int = None
    link: str = None


class ProshopSpider(scrapy.Spider):
    name = 'Proshop_Spider'
    allowed_domains = ['proshop.dk']

    def __init__(self, product_name=None, *args, **kwargs):
        super(ProshopSpider, self).__init__(*args, **kwargs)
        self.product_name = product_name
        self.url = "https://www.proshop.dk/"
        self.products = []

    def start_requests(self):
        if self.product_name:
            url = f'{self.url}?s={self.product_name.replace(" ", "+")}'
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # Your parsing logic here
        for product_li in response.xpath('//ul[@id="products"]/li[contains(@class, "row toggle")]'):
            name_element = product_li.xpath('.//a[@class="site-product-link"]/h2/text()').get()
            info_element = product_li.xpath('.//div[@class="truncate-overflow"]/text()').get()
            price_element = product_li.xpath('.//span[contains(@class,"site-currency-lg")]/text()').get()
            link_element = response.urljoin(product_li.xpath('.//a[contains(@class,"site-product-link")]/@href').get())

            self.products.append(Product(name_element, info_element, price_element, link_element))

    """
        Following function connects the spider_closed signal to the spider_closed method.
        :param crawler: The crawler object that will be used to connect the signal to the method.
    """
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ProshopSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    """
        Following function is called when the spider is closed. 
        It prints the products scraped by the spider.
    """

    def spider_closed(self, reason):
        if reason == 'finished':
            for i, product in enumerate(self.products):
                print(f'{i + 1}: Name: {product.name}\nInfo: {product.info}\nPrice: {product.price}\nLink: {product.link}')
        else:
            print(f'Spider closed with reason: {reason}')

    async def run(self, ctx, product_name=None):
        try:
            if product_name is None:
                await ctx.send("Please provide a product name.")
                return

            products = self.products

            if products:
                with open(f'Proshop{product_name}.txt', 'w') as f:
                    for i, product in enumerate(products[:20]):
                        product_str = (f"Product {i + 1}: "
                                       f"{product.name}\n"
                                       f"Info: {product.info}\n"
                                       f"Price: {product.price}\n"
                                       f"Link: {product.link}\n\n")
                        f.write(product_str)
                await ctx.send(file=discord.File(f'PriceRunner{product_name}.txt'))
                os.remove(f'PriceRunner{product_name}.txt')
            else:
                await ctx.send("No results found for the provided product.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def proshop(self, ctx, product_name=None):
        await self.run(ctx, product_name)

    @proshop.error
    async def proshop_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `!proshop <product_name>`")
        else:
            await ctx.send(f"An error occurred: {error}")


async def setup(bot):
    await bot.add_cog(ProshopSpider(bot))
