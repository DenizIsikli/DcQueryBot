import os
import asyncio
import discord
from discord.ext import commands
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip


class SoundCompressionMP3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @staticmethod
    async def sound_compression_mp3(ctx, link: str = None):
        if ctx.author == ctx.bot.user:
            return

        yt = YouTube(link)

        video_stream = yt.streams.get_highest_resolution()
        yt_title = yt.title
        video_path = video_stream.download()

        # Convert the video to MP3
        video_clip = VideoFileClip(video_path)
        audio_clip = video_clip.audio
        mp3_filename = f'{yt_title}.mp3'
        audio_clip.write_audiofile(mp3_filename)

        # Clean up temporary video file
        video_clip.close()
        audio_clip.close()

        await ctx.message.delete()
        await asyncio.sleep(0.2)
        await ctx.send(file=discord.File(mp3_filename))

        os.remove(video_path)
        os.remove(mp3_filename)

    @commands.command()
    async def mp3(self, ctx, link: str = None):
        await self.sound_compression_mp3(ctx, link)

    @mp3.error
    async def mp3_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `!qrcode <link>`")
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
        await ctx.send(file=discord.File(video_path))

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
