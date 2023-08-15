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
                        value="!wiki {int: article amount} {search query}\nExample: *!wiki Github* || *!wiki 2 Github*",
                        inline=False
        )
        embed.add_field(
            name="**!urban**",
            value="!urban {int: word amount} {search query}\nExample: *!urban Shookie* || *!urban 2 Shookie*",
            inline=False
        )

        # ** ADD NEW COMMANDS TO EMBED **

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(HelpEmbed(bot))
