import os
from discord import FFmpegPCMAudio
from discord.ext import commands
import asyncio
import aiohttp


class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.TEXTTOSPEECH_API = "https://text-to-speech-for-28-languages.p.rapidapi.com/"

    async def text_to_speech(self, ctx, vc, *, content: str = ""):
        if ctx.author == ctx.bot.user:
            return
        print("hi im here")
        if ctx.author.voice is None:
            await ctx.send("You need to be inside a voice channel to use this command.")
            return

        if content is None or content.strip() == "":
            await ctx.send("Please provide the text you want to convert to speech.")
            return

        try:
            headers = {
                "content-type": "application/x-www-form-urlencoded",
                "X-RapidAPI-Key": "2ba10896fdmsh6eb24b198a7b520p1fef74jsneb8afa07df45",
                "X-RapidAPI-Host": "text-to-speech-for-28-languages.p.rapidapi.com"
            }

            payload = {
                "msg": content,
                "lang": "Salli",
                "source": "ttsmp3"
            }

            print("before post")
            async with aiohttp.ClientSession() as session:
                async with session.post(self.TEXTTOSPEECH_API, data=payload, headers=headers) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_data = await response.json()

                    print(response_data)
                    print(response.content_type)

                    # audio_data = response_data["audioContent"]
                    # audio_filename = "tts_audio.ogg"
                    # with open(audio_filename, "wb") as audio_file:
                    #     audio_file.write(audio_data)
                    #
                    # if vc is not None and not vc.is_playing():
                    #     await asyncio.sleep(3)
                    #     await ctx.message.delete()
                    #     vc.play(FFmpegPCMAudio(audio_filename))

        except Exception as e:
            await ctx.send(f"Failed to save the text to audio: {e}")

    @commands.command()
    async def tts(self, ctx, *, content: str = None):
        vc = ctx.author.voice.channel
        await self.text_to_speech(ctx, vc, content=content)

    @tts.error
    async def tts_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide the text you want to convert to speech.")


async def setup(bot):
    await bot.add_cog(TextToSpeech(bot))
