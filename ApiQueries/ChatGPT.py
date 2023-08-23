import asyncio
import aiohttp
from discord.ext import commands


class ChatGPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.CHAT_GPT_API = "https://open-ai21.p.rapidapi.com/conversationllama"

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
                "X-RapidAPI-Host": "open-ai21.p.rapidapi.com"
            }

            payload = {
                "messages": [
                    {
                        "role": "user",
                        "content": content
                    }
                ],
                "web_access": False
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.CHAT_GPT_API, json=payload, headers=headers) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_data = await response.json()

                    ai_response = response_data.get('LLAMA')  # Extract the AI response
                    if ai_response:
                        await ctx.send(f"ChatGPT: {ai_response[:40]}")
                    else:
                        await ctx.send("The AI couldn't provide a response.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def chat(self, ctx, *, content: str = None):
        await self.chat_gpt(ctx, content=content)


async def setup(bot):
    await bot.add_cog(ChatGPT(bot))
