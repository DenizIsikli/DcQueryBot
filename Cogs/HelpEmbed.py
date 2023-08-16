import discord
from discord.ext import commands
import datetime


class HelpEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            title="Command List",
            color=discord.Color.purple()
        )
        embed.add_field(
                        name="**!wiki**",
                        value="!wiki {int: article amount} {str: search query}\n"
                              "Example: *!wiki Github* || *!wiki 2 Github*",
                        inline=False
        )
        embed.add_field(
            name="**!urban**",
            value="!urban {int: word amount} {str: search query}\n"
                  "Example: *!urban Shookie* || *!urban 2 Shookie*",
            inline=False
        )
        embed.add_field(
            name="**!qrcode**",
            value="!qrcode {link}\n"
                  "Example: *!qrcode GitHub.com*",
            inline=False
        )
        embed.add_field(
            name="**!imgur**",
            value="!imgur {str: search query}\n"
                  "Example: *!imgur cat*",
            inline=False
        )
        embed.add_field(
            name="**!ascii**",
            value="!ascii {str: text}\n"
                  "Example: *!ascii placeholder*",
            inline=False
        )
        embed.add_field(
            name="**!asciicm**",
            value="!asciicm {str: text}\n"
                  "Example: *!asciicm placeholder*\n"
                  "`asciicm does not take numbers as an argument, only text`"
        )

        # ** ADD NEW COMMANDS TO EMBED **

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpEmbed(bot))
