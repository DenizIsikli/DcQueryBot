from discord import FFmpegPCMAudio
from discord.ext import commands
import asyncio
import aiohttp
import discord


class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.TEXTTOSPEECH_API = "https://cloudlabs-text-to-speech.p.rapidapi.com/synthesize"

    async def text_to_speech(self, ctx, *, content: str = ""):
        if ctx.author == ctx.bot.user:
            return

        if ctx.author.voice is None:
            await ctx.send("You need to be inside a voice channel to use this command.")
            return

        if content is None or content.strip() == "":
            await ctx.send("Please provide the text you want to convert to speech.")
            return

        try:
            payload = {
                "voice_code": "en-US-1",
                "text": content,
                "speed": "1.00",
                "pitch": "1.00",
                "output_type": "audio_url"
            }

            headers = {
                "content-type": "application/x-www-form-urlencoded",
                "X-RapidAPI-Key": "f4093ae77fmsh3b5b518992b9c97p136562jsn8eb575f33b51",
                "X-RapidAPI-Host": "cloudlabs-text-to-speech.p.rapidapi.com"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(self.TEXTTOSPEECH_API, data=payload, headers=headers) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_data = await response.json()

                    audio_url = response_data["result"]["audio_url"]
                    # send the mp3 as an attachment
                    await ctx.send(audio_url)

        except Exception as e:
            await ctx.send(f"Failed to save the text to audio: {e}")

    @commands.command()
    async def tts(self, ctx, *, content: str = None):
        await self.text_to_speech(ctx, content=content)

    @tts.error
    async def tts_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide the text you want to convert to speech.")


async def setup(bot):
    await bot.add_cog(TextToSpeech(bot))
