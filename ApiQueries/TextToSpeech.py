from discord import FFmpegPCMAudio
from discord.ext import commands
import asyncio
import aiohttp


class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.TEXTTOSPEECH_API = "https://text-to-speech27.p.rapidapi.com/speech"

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
            headers = {
                "X-RapidAPI-Key": "2ba10896fdmsh6eb24b198a7b520p1fef74jsneb8afa07df45",
                "X-RapidAPI-Host": "text-to-speech27.p.rapidapi.com"
            }

            querystring = {"text": f"{content}", "lang": "en-us"}

            async with aiohttp.ClientSession() as session:
                async with session.get(self.TEXTTOSPEECH_API, headers=headers, params=querystring) as response:
                    response.raise_for_status()  # Raise an exception if the request was not successful
                    response_data = await response.json()
                    print(response_data)
                    print("test")

                    vc = ctx.author.voice.channel
                    await vc.connect()

                    vc.play(FFmpegPCMAudio(response_data["audio_url"]))
                    while vc.is_playing():
                        await asyncio.sleep(1)
                    await vc.disconnect()

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
