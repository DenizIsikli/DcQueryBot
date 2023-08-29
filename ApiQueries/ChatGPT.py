import aiohttp
from discord.ext import commands


class ChatGPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.CHAT_GPT_API = "https://simple-chatgpt-api.p.rapidapi.com/ask"

    async def chat_gpt(self, ctx, *, content: str = None):
        if ctx.author == ctx.bot.user:
            return

        if content is None:
            await ctx.send("Please provide text when using the command.")
            return

        try:
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": "2ba10896fdmsh6eb24b198a7b520p1fef74jsneb8afa07df45",
                "X-RapidAPI-Host": "simple-chatgpt-api.p.rapidapi.com"
            }

            payload = {"question": content}

            async with aiohttp.ClientSession() as session:
                async with session.post(self.CHAT_GPT_API, json=payload, headers=headers) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_data = await response.json()

                    ai_response = response_data.get('answer', 'No response from the AI')

                    await ctx.send(ai_response)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def gpt(self, ctx, *, content: str = None):
        await self.chat_gpt(ctx, content=content)


async def setup(bot):
    await bot.add_cog(ChatGPT(bot))
