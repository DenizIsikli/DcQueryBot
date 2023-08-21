import discord
from discord.ext import commands
import datetime


class HelpEmbedMain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def help_embed_main(ctx):
        if ctx.author == ctx.bot.user:
            return

        embed = discord.Embed(
            title="__Main Command List__",
            color=discord.Color.purple()
        )
        embed.add_field(
            name="**!help1**",
            value="First command list.",
            inline=False
        )
        embed.add_field(
            name="**!help2**",
            value="Second command list.",
            inline=False
        )
        embed.add_field(
            name="**!help3**",
            value="Third command list.",
            inline=False
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        await self.help_embed_main(ctx)

    @help.error
    async def help_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


class HelpEmbed1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def help_embed_1(ctx):
        if ctx.author == ctx.bot.user:
            return

        embed = discord.Embed(
            title="__1st Command List__",
            color=discord.Color.purple()
        )
        embed.add_field(
            name="**!wiki**",
            value="Description: Sends a specified amount of 1-5 articles from Wikipedia "
                  "based on the given search query\n"
                  "!wiki {int: article amount} {str: search query}\n"
                  "Example: *!wiki Lev Landau* | *!wiki 2 Lev Landau*",
            inline=False
        )
        embed.add_field(
            name="**!urban**",
            value="Description: Sends a specified amount of 1-5 words from Urban Dictionary "
                  "based on the given search query\n"
                  "!urban {int: word amount} {str: search query}\n"
                  "Example: *!urban Shookie* | *!urban 2 Shookie*",
            inline=False
        )
        embed.add_field(
            name="**!qrcode**",
            value="Description: Creates a Qr-Code based on the given link\n"
                  "!qrcode {link}\n"
                  "Example: *!qrcode GitHub.com*",
            inline=False
        )
        embed.add_field(
            name="**!imgur**",
            value="Description: Sends a random GIF from Imgur based on the given category\n"
                  "!imgur {str: search query}\n"
                  "Example: *!imgur cat*",
            inline=False
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def help1(self, ctx):
        await self.help_embed_1(ctx)

    @help1.error
    async def help1_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


class HelpEmbed2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def help_embed_2(ctx):
        embed = discord.Embed(
            title="__2nd Command List__",
            color=discord.Color.purple()
        )
        embed.add_field(
            name="**!mp3**",
            value="Description: Converts a YouTube video into a MP3 file based on the given link\n"
                  "!mp3 {link}\n"
                  "Example: *!mp3 `https://www.youtube.com/watch?v=HAZoLuME-PU`*",
            inline=False
        )
        embed.add_field(
            name="**!mp4**",
            value="Description: Converts a YouTube video into a MP4 file based on the given link\n"
                  "!mp4 {link}\n"
                  "Example: *!mp4 `https://www.youtube.com/watch?v=HAZoLuME-PU`*",
            inline=False
        )
        embed.add_field(
            name="**!ascii**",
            value="Description: Creates ASCII art based on the given text\n"
                  "!ascii {str: text}\n"
                  "Example: *!ascii placeholder*",
            inline=False

        )
        embed.add_field(
            name="**!asciicm**",
            value="Description: Creates ASCII art with CyberModule font based on the given text\n"
                  "!asciicm {str: text}\n"
                  "Example: *!asciicm placeholder*\n"
                  "`asciicm does not take numbers as an argument, only text`",
            inline=False
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def help2(self, ctx):
        await self.help_embed_2(ctx)

    @help2.error
    async def help2_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


class HelpEmbed3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def help_embed_3(ctx):
        embed = discord.Embed(
            title="__3rd Command List__",
            color=discord.Color.purple()
        )
        embed.add_field(
            name="**!tts**",
            value="Description: Text to speech based on the given text\n"
                  "!tts {str: text}\n"
                  "Example: *!tts Text to speech*\n",
            inline=False
        )
        embed.add_field(
            name="**!reminder**",
            value="Description: Places a reminder based on the given duration in minutes, and text\n"
                  "!reminder {int: duration} {str: reminder}\n"
                  "Example: *!reminder 25 Check the oven*\n",
            inline=False
        )
        embed.add_field(
            name="**!nick**",
            value="Description: Changes your nickname on the server based on the given text\n"
                  "!nick {str: text}\n"
                  "Example: *!nick Bobby*\n",
            inline=False
        )
        embed.add_field(
            name="**!whois**",
            value="Description: Gives a thorough description of the person you @ - "
                  "No @ defaults to yourself\n"
                  "!whois {discord.Member: member}\n"
                  "Example: *!whois @Bobby* | *!whois*\n",
            inline=False
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def help3(self, ctx):
        await self.help_embed_3(ctx)

    @help3.error
    async def help3_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


async def setup(bot):
    await bot.add_cog(HelpEmbedMain(bot))
    await bot.add_cog(HelpEmbed1(bot))
    await bot.add_cog(HelpEmbed2(bot))
    await bot.add_cog(HelpEmbed3(bot))
