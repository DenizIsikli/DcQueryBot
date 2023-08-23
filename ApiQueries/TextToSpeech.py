import os
from discord import FFmpegPCMAudio
from discord.ext import commands
import asyncio
import aiohttp


class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.TEXTTOSPEECH_API = "https://text-to-speech27.p.rapidapi.com/speech"

    async def text_to_speech(self, ctx, vc, *, text: str = ""):
        if ctx.author == ctx.bot.user:
            return

        if ctx.author.voice is None:
            await ctx.send("You need to be inside a voice channel to use this command.")
            return

        if text is None or text.strip() == "":
            await ctx.send("Please provide the text you want to convert to speech.")
            return

        try:
            headers = {
                "X-RapidAPI-Key": "bd4d41a763msh8a45e7e4dfda107p18423bjsnd27abce669f5",
                "X-RapidAPI-Host": "text-to-speech27.p.rapidapi.com"
            }

            query_params = {
                "text": text,
                "lang": "en-us"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.TEXTTOSPEECH_API, headers=headers, params=query_params) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_data = await response.json()

                    audio_data = response_data["audioContent"]
                    audio_filename = "tts_audio.ogg"
                    with open(audio_filename, "wb") as audio_file:
                        audio_file.write(audio_data)

                    if vc is not None and not vc.is_playing():
                        await asyncio.sleep(3)
                        await ctx.message.delete()
                        vc.play(FFmpegPCMAudio(audio_filename))

        except Exception as e:
            await ctx.send(f"Failed to save the text to audio: {e}")
        finally:
            if os.path.exists(audio_filename):
                os.remove(audio_filename)

    @commands.command()
    async def tts(self, ctx, *, text: str = None):
        vc = ctx.author.voice.channel
        await self.text_to_speech(ctx, vc, text=text)

    @tts.error
    async def tts_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide the text you want to convert to speech.")


async def setup(bot):
    await bot.add_cog(TextToSpeech(bot))
