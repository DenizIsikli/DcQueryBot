import discord
from discord.ext import commands
import datetime
from datetime import datetime


class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def server_info(ctx):
        try:
            guild = ctx.guild
            total_members = guild.member_count
            bots = sum(1 for member in guild.members if member.bot)
            actual_members = total_members - bots
            boost_level = guild.premium_tier
            boost_count = guild.premium_subscription_count

            embed = discord.Embed(
                title=f"{guild.name} Server Information",
                color=discord.Color.dark_theme()
            )

            embed.add_field(name="Total Members", value=total_members, inline=True)
            embed.add_field(name="Actual members", value=actual_members, inline=True)
            embed.add_field(name="Bots", value=bots, inline=True)
            embed.add_field(name="Server Boost Level", value=boost_level, inline=True)
            embed.add_field(name="Total Boosts", value=boost_count, inline=True)
            embed.add_field(name="Server Creation Date", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)

            # Add & set footer with timestamp
            timestamp = datetime.utcnow()
            embed.timestamp = timestamp
            embed.set_footer(text=f"Requested by {ctx.author.name}")

            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def serverinfo(self, ctx):
        await self.server_info(ctx)

    @serverinfo.error
    async def serverinfo_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("An error occurred while processing your request.")
        else:
            await ctx.send("An error occurred.")


class WhoIs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def who_is(ctx, member: discord.Member = None):
        try:
            if ctx.author == ctx.bot.user:
                return

            # If member not specified, default to author
            member = member or ctx.author

            embed = discord.Embed(
                title=f"Who is {member.display_name}",
                color=discord.Color.dark_theme()
            )

            embed.set_thumbnail(url=member.display_avatar)

            embed.add_field(name="**ID:**", value=member.id)
            embed.add_field(name="**Name:**", value=member.display_name)

            embed.add_field(name="**Created Account On:**", value=member.created_at.strftime("%Y-%m-%d | %H:%M:%S"))
            embed.add_field(name="**Joined Server On:**", value=member.joined_at.strftime("%Y-%m-%d | %H:%M:%S"))

            roles = ', '.join(role.name for role in member.roles)
            embed.add_field(name="**Roles:**", value=roles)

            embed.add_field(name="**Highest Role:**", value=member.top_role)

            # Add & set footer with timestamp
            timestamp = datetime.utcnow()
            embed.timestamp = timestamp
            embed.set_footer(text=f"Requested by {ctx.author.name}")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):
        await self.who_is(ctx, member=member)

    @whois.error
    async def whois_error(self, ctx, error):
        if isinstance(error, commands.UserNotFound):
            await ctx.send("User not found. Please provide a valid user mention or ID.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument. Please provide a valid user mention or ID.")
        else:
            await ctx.send("An error occurred while processing your request.")


async def setup(bot):
    await bot.add_cog(ServerInfo(bot))
    await bot.add_cog(WhoIs(bot))
