import os
import asyncio
import discord
from io import BytesIO
from pytube import YouTube
from discord.ext import commands


class SoundCompressionMP3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def sound_compression_mp3(ctx, link: str = None):
        if ctx.author == ctx.bot.user:
            return

        yt = YouTube(link)
        yt_title = yt.title

        audio_stream = yt.streams.filter(only_audio=True).first()
        audio_buffer = BytesIO()
        audio_stream.stream_to_buffer(audio_buffer)
        audio_buffer.seek(0)

        mp3_filename = f"{yt_title}.mp3"

        await ctx.message.delete()
        await asyncio.sleep(0.2)
        await ctx.send(file=discord.File(audio_buffer, filename=mp3_filename))

        audio_buffer.close()  # Clear the buffer

    @commands.command()
    async def mp3(self, ctx, link: str = None):
        await self.sound_compression_mp3(ctx, link)

    @mp3.error
    async def mp3_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `!mp3 <link>`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Please provide a valid link.")
        else:
            await ctx.send(f"An error occurred: {error}")


class SoundCompressionMP4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def sound_compression_mp4(ctx, link: str = None):
        if ctx.author == ctx.bot.user:
            return

        yt = YouTube(link)

        video_stream = yt.streams.filter(file_extension='mp4', progressive=True).order_by('resolution').desc().first()
        video_path = video_stream.download()

        await ctx.message.delete()
        await asyncio.sleep(0.2)

        # Check if the video file size is within Discord limits
        file_size = os.path.getsize(video_path) / (1024 * 1024)  # Convert to MB
        if file_size <= 8:
            await ctx.send(file=discord.File(video_path))
        else:
            await ctx.send("The video file is too large to send.")

        os.remove(video_path)

    @commands.command()
    async def mp4(self, ctx, link: str = None):
        await self.sound_compression_mp4(ctx, link)

    @mp4.error
    async def mp4_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `!qrcode <link>`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Please provide a valid link.")
        else:
            await ctx.send(f"An error occurred: {error}")


async def setup(bot):
    await bot.add_cog(SoundCompressionMP3(bot))
    await bot.add_cog(SoundCompressionMP4(bot))
