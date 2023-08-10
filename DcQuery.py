import discord
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
    async def delete(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)


class Setup(commands.Cog):
    def __init__(self):
        pass

    @staticmethod
    async def setup(bot):
        await bot.add_cog(AdminDelete())
