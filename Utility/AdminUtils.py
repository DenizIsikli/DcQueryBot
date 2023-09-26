import os
import discord
from discord.ext import commands
import datetime


class AdminEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def admin(self, ctx):
        embed = discord.Embed(
            title="Admin Command List",
            color=discord.Color.orange()
        )
        embed.add_field(name="**!delete**", value="*Delete x amount of channel messages: default amount = 1*")
        embed.add_field(name="**!kick**", value="*Kick specified member: reason[optional]*")
        embed.add_field(name="**!reload**", value="*Reload all Cog files*")

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)


class AdminDelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def delete(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            command_owner = ctx.bot.get_user(ctx.bot.owner_id)
            await ctx.send(f"Missing permission! - Permission assigned to {command_owner}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument")


class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason="No reason provided"
        await ctx.guild.kick(member)
        await ctx.send(f"User {member.mention} has been kicked\nReason: {reason}")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            command_owner = ctx.bot.get_user(ctx.bot.owner_id)
            await ctx.send(f"Missing permission! - Permission assigned to {command_owner}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument")


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx):
        async with ctx.typing():
            embed = discord.Embed(
                title="Reloading all cogs!",
                color=discord.Color.green()
            )

            # Add & set footer with timestamp
            timestamp = datetime.datetime.utcnow()
            embed.timestamp = timestamp
            embed.set_footer(text=f"Requested by {ctx.author.name}")

            # List for reloaded cogs
            reloaded_queries = []
            reloaded_cogs = []
            reloaded_util = []

            try:
                try:
                    for filename in os.listdir("../ApiQueries"):
                        if filename.endswith(".py"):
                            query_name = f"Cogs.{filename[:-3]}"  # Remove the last 3 characters (.py)
                            try:
                                await self.bot.unload_extensionload_extension(query_name)
                                await self.bot.load_extension(query_name)
                                reloaded_queries.append(query_name)
                            except Exception as e:
                                print(f"Failed to reload Query file: {query_name}: {e}")
                except Exception as e:
                    print(f"Failed to reload any Query files: {e}")

                try:
                    for filename in os.listdir("../Cogs"):
                        if filename.endswith(".py"):
                            cog_name = f"Cogs.{filename[:-3]}"  # Remove the last 3 characters (.py)
                            try:
                                await self.bot.unload_extension(cog_name)
                                await self.bot.load_extension(cog_name)
                                reloaded_cogs.append(cog_name)
                            except Exception as e:
                                print(f"Failed to reload Cog file: {cog_name}: {e}")
                except Exception as e:
                    print(f"Failed to reload any Cog files: {e}")

                try:
                    for filename in os.listdir("../Utility"):
                        if filename.endswith(".py"):
                            util_name = f"Utility.{filename[:-3]}"  # Remove the last 3 characters (.py)
                            try:
                                await self.bot.unload_extension(util_name)
                                await self.bot.load_extension(util_name)
                                reloaded_util.append(util_name)
                            except Exception as e:
                                print(f"Failed to reload Util file: {util_name}: {e}")
                except Exception as e:
                    print(f"Failed to reload any Utility files: {e}")

                if reloaded_cogs:
                    embed.add_field(
                        name="Reloaded Cog Files",
                        value="\n".join(reloaded_cogs)
                    )
                if reloaded_util:
                    embed.add_field(
                        name="Reloaded Util Files",
                        value="\n".join(reloaded_util)
                    )
            except Exception as e:
                print(f"Failed to find any files: {e}")

        await ctx.send(embed=embed)


class Mute(commands.Cog):
    @commands.command()
    @commands.is_owner()
    async def mute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(muted_role, send_messages=False)

        await member.add_roles(muted_role)

    @commands.command()
    @commands.is_owner()
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role and muted_role in member.roles:
            await member.remove_roles(muted_role)
        else:
            await ctx.send("User is not muted")


async def setup(bot):
    # Util commands
    await bot.add_cog(Reload(bot))

    # Admin commands
    await bot.add_cog(AdminDelete(bot))
    await bot.add_cog(Kick(bot))

    # Embed commands
    await bot.add_cog(AdminEmbed(bot))

    # Mute commands
    await bot.add_cog(Mute(bot))
