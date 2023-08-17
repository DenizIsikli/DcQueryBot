import discord
from discord.ext import commands
import datetime


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def who_is(ctx, member: discord.Member = None):
        if ctx.author == ctx.bot.user:
            return

        member = member or ctx.author

        embed = discord.Embed(
            title=f"Who is {member.display_name}",
            color=discord.Color.dark_theme()
        )
        embed.set_thumbnail(url=member.avatar_url)

        embed.add_field(name="**ID:**", value=member.id)
        embed.add_field(name="**Name:**", value=member.display_name)

        embed.add_field(name="**Created Account On:**", value=member.created_at)
        embed.add_field(name="**Joined Server On:**", value=member.joined_at)

        embed.add_field(name="**Roles:**", value=member.roles)
        embed.add_field(name="**Highest Role:", value=member.top_role)

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):
        await self.who_is(ctx, member)

    @whois.error
    async def whois_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument")


async def setup(bot):
    await bot.add_cog(Miscellaneous(bot))
