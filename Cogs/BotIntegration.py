from discord.ext import commands


class GitHub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def bot_owner(ctx):
        await ctx.send("https://github.com/DenizIsikli")

    @commands.command()
    async def owner(self, ctx):
        await self.bot_owner(ctx)

    @staticmethod
    async def bot_picture(ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/826814606298316882/1142173434567200869/love.png")

    @commands.command()
    async def botpic(self, ctx):
        await self.bot_picture(ctx)

    @staticmethod
    async def bot_repository(ctx):
        await ctx.send("https://github.com/DenizIsikli/DcQueryBot")

    @commands.command()
    async def repo(self, ctx):
        await self.bot_repository(ctx)

    @commands.command()
    async def website(self, ctx):
        await ctx.send("https://uselessbotwebsite.netlify.app/")


async def setup(bot):
    await bot.add_cog(GitHub(bot))
