import os
import discord
import datetime
from discord.ext import commands


class Intents:
    @staticmethod
    def create_intents():
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guild_messages = True
        intents.dm_messages = True
        return intents


intents_instance = Intents.create_intents()


class HelpEmbed(commands.Cog):
    @commands.command(intents=intents_instance)
    async def help(self, ctx, message: discord.Message):
        embed = discord.Embed(
            title="Command List",
            color=discord.Color.purple()
        )
        embed.add_field(
                        name="**!wiki**",
                        value="!wiki {int: article amount} {search query}\nExample: *!wiki Github* || *!wiki 2 Github*"
        )
        embed.add_field(
            name="**!urban**",
            value="!urban {int: word amount} {search query}\nExample: *!urban Shookie* || *!urban 2 Shookie*"
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {message.author.name}")

        await ctx.send(embed=embed)


class AdminEmbed(commands.Cog):
    @commands.command(intents=intents_instance)
    @commands.is_owner()
    async def admin(self, ctx, message: discord.Message):
        embed = discord.Embed(
            title="Admin Command List",
            color=discord.Color.orange()
        )
        embed.add_field(name="**!delete**", value="*Delete x amount of channel messages: default amount = 1*")
        embed.add_field(name="**!kick**", value="*Kick specified member: reason[optional]")
        embed.add_field(name="**!reload**", value="*Reload all Cog files*")

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {message.author.name}")

        await ctx.send(embed=embed)


class AdminDelete(commands.Cog):
    @commands.command(intents=intents_instance)
    @commands.is_owner()
    async def delete(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)

    @delete.error
    async def delete_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            command_owner = commands.is_owner()
            await ctx.send(f"Missing permission! - Permission assigned to {command_owner}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument")


class Kick(commands.Cog):
    @commands.command(intents=intents_instance)
    @commands.is_owner()
    async def kick(self, member, *, reason=None):
        await member.kick(reason=reason)

    @kick.error
    async def kick_error(self, error, ctx):
        if isinstance(error, commands.MissingPermissions):
            command_owner = commands.is_owner()
            await ctx.send(f"Missing permission! - Permission assigned to {command_owner}")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument")


class Reload(commands.Cog):
    def __init__(self):
        self.bot = commands.Bot

    @commands.command(intents=intents_instance)
    @commands.is_owner()
    async def reload(self, ctx, bot, message: discord.Message):
        async with ctx.typing():
            embed = discord.Embed(
                title="Reloading all cogs!",
                color=discord.Color.green()
            )

            # Add & set footer with timestamp
            timestamp = datetime.datetime.utcnow()
            embed.timestamp = timestamp
            embed.set_footer(text=f"Requested by {message.author.name}")

            try:
                for filename in os.listdir("Cogs"):
                    if filename.endswith(".py"):
                        try:
                            await bot.unload_extension(f"Cogs.{filename}")
                            await bot.load_extension(f"Cogs.{filename}")
                            embed.add_field(
                                name=f"Reloaded: {filename}",
                                value='\uFeFF'
                            )
                        except Exception as e:
                            print(f"Failed to reload cog: Cogs.{filename}: {e}")
            except Exception as e:
                print(f"Failed to find the cog files: {e}")

            await ctx.send(embed=embed)


class Setup(commands.Cog):
    def __init__(self):
        pass

    @staticmethod
    async def setup(bot):
        # Util commands
        await bot.add_cog(Reload())

        # Admin commands
        await bot.add_cog(AdminDelete())
        await bot.add_cog(Kick())

        # Embed commands
        await bot.add_cog(HelpEmbed())
        await bot.add_cog(AdminEmbed())
