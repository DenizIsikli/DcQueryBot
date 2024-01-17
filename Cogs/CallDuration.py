from discord.ext import commands
from datetime import datetime


class VoiceDurationTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_channel_join_times = {}  # Dictionary to track join times

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # User joins a voice channel
        if after.channel and not before.channel:
            self.voice_channel_join_times[member.id] = datetime.now()

        # User leaves a voice channel
        if before.channel and not after.channel:
            if member.id in self.voice_channel_join_times:
                del self.voice_channel_join_times[member.id]

    @commands.command()
    async def callduration(self, ctx):
        member = ctx.message.author
        if member.id in self.voice_channel_join_times:
            join_time = self.voice_channel_join_times[member.id]
            duration = datetime.now().replace(microsecond=0) - join_time.replace(microsecond=0)
            await ctx.send(f"{member.display_name}, you've been in the call for {duration}")
        else:
            await ctx.send("You're not currently in a voice channel.")


async def setup(bot):
    await bot.add_cog(VoiceDurationTracker(bot))
