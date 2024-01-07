import asyncio
from discord.ext import commands


class Pomodoro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pomodoro_tasks = {}

    async def start_pomodoro(self, ctx, study_duration: float, break_duration: float, cycles: int):
        for i in range(cycles):
            await ctx.send(f"{ctx.author.mention} Time to study! 📚")
            await asyncio.sleep(study_duration * 60)

            if ctx.author.id in self.pomodoro_tasks and self.pomodoro_tasks[ctx.author.id].cancelled():
                break

            await ctx.send(f"{ctx.author.mention} Time for a break! ☕")
            await asyncio.sleep(break_duration * 60)

        if ctx.author.id in self.pomodoro_tasks:
            del self.pomodoro_tasks[ctx.author.id]

    @commands.command()
    async def pomodoro(self, ctx, study_duration: float = 25, break_duration: float = 5, cycles: int = 4):
        if study_duration <= 0 or break_duration <= 0 or cycles <= 0:
            await ctx.send("Please enter valid values for duration and cycles.")
            return

        if ctx.author.id in self.pomodoro_tasks:
            self.pomodoro_tasks[ctx.author.id].cancel()

        task = asyncio.create_task(self.start_pomodoro(ctx, study_duration, break_duration, cycles))
        self.pomodoro_tasks[ctx.author.id] = task

    @commands.command()
    async def pomodorostop(self, ctx):
        if ctx.author.id in self.pomodoro_tasks:
            self.pomodoro_tasks[ctx.author.id].cancel()
            await ctx.send(f"{ctx.author.mention} Pomodoro stopped. You can start a new one anytime.")
        else:
            await ctx.send(f"{ctx.author.mention} There is no active Pomodoro to stop.")


async def setup(bot):
    await bot.add_cog(Pomodoro(bot))
