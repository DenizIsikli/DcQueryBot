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


class AdminDelete(commands.Cog):
    @commands.command(intents=intents_instance)
    @commands.is_owner()
    async def delete(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)


class Reload(commands.Cog):
    def __init__(self):
        self.bot = commands.Bot

    @commands.command(intents=intents_instance)
    @commands.is_owner()
    async def reload(self, ctx, bot, message: discord.Message):
        async with ctx.typing():
            embed = discord.Embed(
                title="Reloading all cogs!",
                color=discord.Color.green(),

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
        await bot.add_cog(AdminDelete())
        await bot.add_cog(Reload())
