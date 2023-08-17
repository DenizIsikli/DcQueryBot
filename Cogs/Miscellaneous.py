import discord
from discord.ext import commands
import datetime


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def who_is(ctx, member: discord.Member = None):
        print("im inside now")
        member = member or ctx.author

        embed = discord.Embed(
            title=f"Who is {member.display_name}",
            color=discord.Color.dark_theme()
        )
        embed.set_thumbnail(url=member.avatar)

        embed.add_field(name="**Name**", value=member.display_name, inline=False)
        embed.add_field(name="**Account Created**", value=member.created_at, inline=False)

        if member.joined_at:
            joined_time = datetime.datetime.now() - member.joined_at
            embed.add_field(name="**Time in Server**", value=str(joined_time), inline=False)

        roles = ", ".join([role.mention for role in member.roles if role != ctx.guild.default_role])
        embed.add_field(name="**Roles**", value=roles, inline=False)

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):
        await self.who_is(ctx.bot, member)

    @whois.error
    async def whois_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument")


async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))
