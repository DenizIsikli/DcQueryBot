from art import *
import discord
from discord.ext import commands


class AsciiArtGenerator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Standard ascii art
    @staticmethod
    async def ascii_art_generator1(bot, message: discord.Message, text: str):
        if message.author == bot.user:
            return

        # Wrap the ASCII art in a code block
        output = text2art(f"{text}", font="small")
        await message.channel.send(f"```\n{output}\n```")

    @commands.command()
    async def ascii(self, ctx, *, text: str):
        await self.ascii_art_generator1(ctx.bot, ctx.message, text)

    # Font: Cybermedium
    @staticmethod
    async def ascii_art_generator2(bot, message: discord.Message, text: str):
        if message.author == bot.user:
            return

        output = text2art(f"{text}", font="cybermedium")
        await message.channel.send(f"```\n{output}\n```")

    @commands.command()
    async def asciicm(self, ctx, *, text: str):
        await self.ascii_art_generator2(ctx.bot, ctx.message, text)


async def setup(bot):
    await bot.add_cog(AsciiArtGenerator(bot))
