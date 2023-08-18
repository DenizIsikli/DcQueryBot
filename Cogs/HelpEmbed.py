import discord
from discord.ext import commands
import datetime


class HelpEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def help_embed(ctx):
        if ctx.author == ctx.bot.user:
            return

        embed = discord.Embed(
            title="Command List",
            color=discord.Color.purple()
        )
        embed.add_field(
            name="**!wiki**",
            value="Description: Sends a Wikipedia article based on the given search query\n"
                  "!wiki {int: article amount} {str: search query}\n"
                  "Example: *!wiki Github* || *!wiki 2 Github*",
            inline=False
        )
        embed.add_field(
            name="**!urban**",
            value="Description: Sends a Word from the Urban Dictionary based on the given search query\n"
                  "!urban {int: word amount} {str: search query}\n"
                  "Example: *!urban Shookie* || *!urban 2 Shookie*",
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
                  "`asciicm does not take numbers as an argument, only text`"
        )

        # ** ADD NEW COMMANDS TO EMBED **

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        await self.help_embed(ctx)

    @help.error
    async def help_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


async def setup(bot):
    await bot.add_cog(HelpEmbed(bot))
