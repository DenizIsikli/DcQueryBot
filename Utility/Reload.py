import os
import datetime
import discord
from discord.ext import commands


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


async def setup(bot):
    await bot.add_cog(Reload(bot))
