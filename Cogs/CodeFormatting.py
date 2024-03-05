from discord.ext import commands


class CodeFormatting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cf'])
    async def codeformat(self, ctx, language: str, *, code: str):
        await ctx.message.delete()
        formatted_message = f"Language Requested: {language}```{language}\n{code}\n```"
        await ctx.send(formatted_message)

    @codeformat.error
    async def codeformat_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You need to provide a language and code to format.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid language provided.")


async def setup(bot):
    await bot.add_cog(CodeFormatting(bot))
