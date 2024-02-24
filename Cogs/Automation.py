import asyncio
import random
import pyautogui
from discord.ext import commands


class AfkAutomation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def afk_automation(ctx, timer: int = 60):
        if ctx.author == ctx.bot.user:
            return

        if timer <= 0:
            await ctx.send("Invalid timer value. Timer must be a positive integer.")
            return

        await ctx.send(f"AFK started for {timer} seconds by {ctx.author.mention} - Type __afkstop__ to stop the timer")

        auto = pyautogui
        x, y = auto.size()

        async def loop_function():
            for duration in range(timer):
                async for message in ctx.channel.history(limit=1):
                    if message.author == ctx.author and message.content.lower() == "afkstop":
                        return True

                x1 = random.randint(0, x)
                y1 = random.randint(0, y)
                auto.moveTo(x1, y1)
                auto.press('f15')
                await asyncio.sleep(1)

            return False

        if await loop_function():
            await ctx.send(f"AFK state stopped by {ctx.author.mention}")
        else:
            await ctx.send(f"Your timer is done: {ctx.author.mention}")

    @commands.command()
    async def afk(self, ctx, timer: int = 60):
        await self.afk_automation(ctx, timer)


async def setup(bot):
    await bot.add_cog(AfkAutomation(bot))
