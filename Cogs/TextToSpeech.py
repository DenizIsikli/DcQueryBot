import os
from discord import FFmpegPCMAudio
from discord.ext import commands
import asyncio
import aiohttp


class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.TEXTTOSPEECH_API = "https://text-to-speech-neural-google.p.rapidapi.com/generateAudioFiles"

    async def text_to_speech(self, ctx, vc, *, text: str = None):
        if ctx.author == ctx.bot.user:
            return

        try:
            headers = {
                "content-type": "application/json",
                "X-RapidAPI-Key": "a923a5ce6emshf1cac57caefd541p1ef8cbjsna3138661f6a7",
                "X-RapidAPI-Host": "text-to-speech-neural-google.p.rapidapi.com"
            }

            payload = {
                "audioFormat": "ogg",
                "paragraphChunks": [
                    f"{text}"],
                "voiceParams": {
                    "name": "Wavenet-B",
                    "engine": "google",
                    "languageCode": "en-IN"
                }
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.TEXTTOSPEECH_API, params=payload, headers=headers) as response:
                    response.raise_for_status()  # Raise an exception if the request was not succesful
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
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("An error occurred while processing your request.")
        else:
            await ctx.send("An error occurred.")


async def setup(bot):
    await bot.add_cog(TextToSpeech(bot))
