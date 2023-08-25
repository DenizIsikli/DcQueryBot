import asyncio
import random
import keyboard
import pyautogui
from discord.ext import commands


class AfkAutomation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.i = 0

    async def afk_automation(self, ctx, timer: int = 60):
        if ctx.author == ctx.bot.user:
            return

        if timer <= 0:
            await ctx.send("Invalid timer value. Timer must be a positive integer.")
            return

        auto = pyautogui
        auto.FAILSAFE = False
        x, y = auto.size()

        async def loop_function():
            while self.i < timer:
                x1 = random.randint(0, x)
                y1 = random.randint(0, y)

                auto.moveTo(x1, y1)

                await asyncio.sleep(1)
                self.i += 1

                if keyboard.is_pressed("f"):
                    return True

            return False

        if await loop_function():
            await ctx.send(f"AFK automation stopped by {ctx.author.mention}")
        else:
            await ctx.send(f"Your timer is done: {ctx.author.mention}")

    @commands.command()
    async def afk(self, ctx, timer: int = 60):
        await self.afk_automation(ctx, timer)


async def setup(bot):
    await bot.add_cog(AfkAutomation(bot))
