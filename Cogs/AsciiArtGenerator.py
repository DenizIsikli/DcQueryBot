from art import *
from discord.ext import commands


class AsciiArtGenerator1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Standard ascii art
    @staticmethod
    async def ascii_art_generator1(ctx, text: str):
        if ctx.author == ctx.bot.user:
            return

        # Wrap the ASCII art in a code block
        output = text2art(f"{text}", font="small")
        await ctx.send(f"```\n{output}\n```")

    @commands.command()
    async def ascii(self, ctx, *, text: str):
        await self.ascii_art_generator1(ctx, text)


class AsciiArtGenerator2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Font: Cybermedium
    @staticmethod
    async def ascii_art_generator2(ctx, text: str):
        if ctx.author == ctx.bot.user:
            return

        output = text2art(f"{text}", font="cybermedium")
        await ctx.send(f"```\n{output}\n```")

    @commands.command()
    async def asciicm(self, ctx, *, text: str):
        if any(char.isdigit() for char in text):
            await ctx.send("This command does not take numbers as an argument.")
            return
        else:
            await self.ascii_art_generator2(ctx, text)


async def setup(bot):
    await bot.add_cog(AsciiArtGenerator1(bot))
    await bot.add_cog(AsciiArtGenerator2(bot))
