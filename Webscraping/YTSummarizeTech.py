import os
import asyncio
from bs4 import BeautifulSoup
import requests
import discord
from discord.ext import commands


class SummarizeTech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url = "https://www.summarize.tech"

    async def yt_summarize_tech(self, ctx, url):
        summary_url = f'{self.url}/video_url={url}'

        response = requests.get(summary_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            video_title = soup.find('div', class_='vstack gap-3').find('h1').find('a').text
            output_file = f'Summary{video_title}.txt'
            summary_section = soup.find('section').find('ul')

            if summary_section:
                with open(output_file, 'w') as f:
                    f.write(f'Video Title: {video_title}\n')
                    f.write(f'URL: {url}\n\n')

                    f.write('\n\n--------------------------------------------------------------------\n\n'.join(
                        [li.text for li in summary_section.find_all('li')])
                    )

                    f.write('\n')

                await ctx.message.delete()
                await asyncio.sleep(0.2)
                await ctx.send(file=discord.File(output_file))
                os.remove(output_file)

        else:
            print(f'Error: {response.status_code}')
            return None

    @commands.command()
    async def summyt(self, ctx, url):
        await self.yt_summarize_tech(ctx, url)

    @summyt.error
    async def summyt_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a YouTube URL")


async def setup(bot):
    await bot.add_cog(SummarizeTech(bot))
