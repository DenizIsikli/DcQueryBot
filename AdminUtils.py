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
    async def kick(self, member, *, reason=None):
        await member.kick(reason=reason)

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
            reloaded_cogs = []
            reloaded_util = []

            try:
                for filename in os.listdir("Cogs"):
                    if filename.endswith(".py"):
                        cog_name = f"Cogs.{filename[:-3]}"  # Remove the last 3 characters (.py)
                        try:
                            await self.bot.unload_extension(cog_name)
                            await self.bot.load_extension(cog_name)
                            reloaded_cogs.append(cog_name)  # Add file to list
                        except Exception as e:
                            print(f"Failed to reload cog files: Cogs.{cog_name}: {e}")
                try:
                    # Loading util file
                    await self.bot.unload_extension("DcQuery")
                    await self.bot.load_extension("DcQuery")
                    reloaded_util.append("DcQuery")
                except Exception as e:
                    print(f"Failed to reload util file: DcQuery: {e}")

                if reloaded_cogs:
                    embed.add_field(
                        name="Reloaded Cogs Files",
                        value="\n".join(reloaded_cogs)
                    )
                if reloaded_util:
                    embed.add_field(
                        name="Reloaded Util File",
                        value="\n".join(reloaded_util)
                    )
            except Exception as e:
                print(f"Failed to find the cog files: {e}")

        await ctx.send(embed=embed)


async def setup(bot):
    # Util commands
    await bot.add_cog(Reload(bot))

    # Admin commands
    await bot.add_cog(AdminDelete(bot))
    await bot.add_cog(Kick(bot))

    # Embed commands
    await bot.add_cog(AdminEmbed(bot))
