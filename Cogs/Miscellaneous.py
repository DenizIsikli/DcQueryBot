import os
import discord
from discord.ext import commands
import datetime
from gtts import gTTS
from mutagen.mp3 import MP3


class WhoIs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def who_is(ctx, member: discord.Member = None):
        if ctx.author == ctx.bot.user:
            return

        member = member or ctx.author

        embed = discord.Embed(
            title=f"Who is {member.display_name}",
            color=discord.Color.dark_theme()
        )
        embed.set_thumbnail(url=member.avatar_url)

        embed.add_field(name="**ID:**", value=member.id)
        embed.add_field(name="**Name:**", value=member.display_name)

        embed.add_field(name="**Created Account On:**", value=member.created_at)
        embed.add_field(name="**Joined Server On:**", value=member.joined_at)

        embed.add_field(name="**Roles:**", value=member.roles)
        embed.add_field(name="**Highest Role:", value=member.top_role)

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):
        await self.who_is(ctx, member)

    @whois.error
    async def whois_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Member not found. Please provide a valid user mention or ID.")
        elif isinstance(error, commands.UserNotFound):
            await ctx.send("User not found. Please provide a valid user mention or ID.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument. Please provide a valid user mention or ID.")
        else:
            await ctx.send("An error occurred while processing your request.")


class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def text_to_speech(ctx, *, text: str = None):
        try:
            if ctx.author.voice and ctx.author.voice.channel:
                speech = gTTS(text=text, lang="en", slow=False, lang_check=True)
                speech.save("speech.mp3")
                audio = MP3("speech.mp3")
                audio_length = audio.info.length

                if audio_length > 0:
                    voice_channel = ctx.author.voice.channel
                    vc = await voice_channel.connect()
                    vc.play(discord.FFmpegPCMAudio("speech.mp3"))
                    await vc.disconnect()
                    os.remove("speech.mp3")
                else:
                    await ctx.send("Failed to generate audio!")
            else:
                await ctx.send("You need to be inside a voice channel to use this command!")
        except Exception as e:
            await ctx.send(f"Failed to save the text to audio: {e}")
            os.remove("speech.mp3")

    @commands.command()
    async def tts(self, ctx, text: str = None):
        await self.text_to_speech(ctx, text=text)

    @tts.error
    async def tts_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide the text you want to convert to speech.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("An error occurred while processing your request.")
        else:
            await ctx.send("An error occurred.")


async def setup(bot):
    await bot.add_cog(WhoIs(bot))
    await bot.add_cog(TextToSpeech(bot))
