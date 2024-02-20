import discord
from discord.ext import commands
import datetime


class AdminEmbedMain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def admin_embed_main(ctx):
        if ctx.author == ctx.bot.user:
            return

        embed = discord.Embed(
            title="__Main Admin Commands__",
            color=discord.Color.dark_theme()
        )
        embed.add_field(
            name="**!admin1**",
            value="First admin command list"
        )
        embed.add_field(
            name="**!admin2**",
            value="Second admin command list"
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def admin(self, ctx):
        await self.admin_embed_main(ctx)

    @admin.error
    async def admin_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


class AdminEmbed1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def admin_embed_1(ctx):
        if ctx.author == ctx.bot.user:
            return

        embed = discord.Embed(
            title="__1st Admin Command List__",
            color=discord.Color.dark_theme()
        )
        embed.add_field(
            name="**!delete**",
            value="Deletes the specified amount of messages\n"
                  "!delete {int: amount} - Default: 1\n"
                  "Example: *!delete 5*",
            inline=False
        )
        embed.add_field(
            name="**!kick**",
            value="Kicks the specified user\n"
                  "!kick {member: user} {str: reason} - Default: None\n"
                  "Example: *!kick @user#1234 Reason: Being a bad user*",
            inline=False
        )
        embed.add_field(
            name="**!reload**",
            value="Reloads all bot files\n"
                  "Example: *!reload*",
            inline=False
        )
        embed.add_field(
            name="**!mute**",
            value="Mutes the specified user\n"
                  "!mute {member: user}\n"
                  "Example: *!mute @user#1234*",
            inline=False
        )
        embed.add_field(
            name="**!unmute**",
            value="Unmutes the specified user\n"
                  "!unmute {member: user}\n"
                  "Example: *!unmute @user#1234*",
            inline=False
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def admin1(self, ctx):
        await self.admin_embed_1(ctx)

    @admin1.error
    async def admin1_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


class AdminEmbed2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def admin_embed_2(ctx):
        if ctx.author == ctx.bot.user:
            return

        embed = discord.Embed(
            title="__2nd Admin Command List__",
            color=discord.Color.dark_theme()
        )
        embed.add_field(
            name="**!addrole**",
            value="Adds the specified role to the specified user\n"
                  "!addrole {role: role} {member: user}\n"
                  "Example: *!addrole @role @user#1234*",
            inline=False
        )
        embed.add_field(
            name="**!delrole**",
            value="Removes the specified role from the specified user\n"
                  "!delrole {role: role} {member: user}\n"
                  "Example: *!delrole @role @user#1234*",
            inline=False
        )
        embed.add_field(
            name="**!createrole**",
            value="Creates a new role\n"
                  "!createrole {str: role_name}\n"
                  "Example: *!createrole NewRole*",
            inline=False
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def admin2(self, ctx):
        await self.admin_embed_2(ctx)

    @admin2.error
    async def admin2_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


async def setup(bot):
    await bot.add_cog(AdminEmbedMain(bot))
    await bot.add_cog(AdminEmbed1(bot))
    await bot.add_cog(AdminEmbed2(bot))
