import os
import discord
from discord.ext import commands
import datetime
import aiohttp
import asyncio
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


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
        if isinstance(error, commands.UserNotFound):
            await ctx.send("User not found. Please provide a valid user mention or ID.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument. Please provide a valid user mention or ID.")
        else:
            await ctx.send("An error occurred while processing your request.")


class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Initialize the IBM Watson Text to Speech client
        authenticator = IAMAuthenticator('YOUR_API_KEY')  # Replace with your API key
        self.client = TextToSpeechV1(authenticator=authenticator)
        self.client.set_service_url('YOUR_SERVICE_URL')  # Replace with your service URL

    async def text_to_speech(self, ctx, *, text: str = None):
        global vc
        try:
            if ctx.author.voice and ctx.author.voice.channel:
                if text is not None and text.strip() != "":
                    response = self.client.synthesize(text, accept='audio/mp3')

                    # Save the audio to a file
                    with open("speech.mp3", "wb") as out_file:
                        out_file.write(response.get_result().content)

                    voice_channel = ctx.author.voice.channel
                    vc = await voice_channel.connect()

                    vc.play(discord.FFmpegPCMAudio("speech.mp3"), after=lambda e: os.remove("speech.mp3"))

                    while vc.is_playing():
                        await asyncio.sleep(1)

                    await vc.disconnect()
                else:
                    await ctx.send("Please provide the text you want to convert to speech.")
            else:
                await ctx.send("You need to be inside a voice channel to use this command!")
        except Exception as e:
            await ctx.send(f"Failed to save the text to audio: {e}")
            await asyncio.sleep(1)
            await vc.disconnect()
            os.remove("speech.mp3")

    @commands.command()
    async def tts(self, ctx, *, text: str = None):
        await self.text_to_speech(ctx, text=text)

    @tts.error
    async def tts_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide the text you want to convert to speech.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("An error occurred while processing your request.")
        elif isinstance(error, aiohttp.ClientOSError):
            await ctx.send("An error occurred while downloading the audio.")
        else:
            await ctx.send("An error occurred.")


class ChangeNickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def change_nickname(ctx, *, new_name: str = None):
        try:
            old_name = ctx.author.display_name
            await ctx.author.edit(nick=new_name)
            await ctx.send(f"Nickname changed from {old_name} to {new_name}")
        except discord.Forbidden:
            await ctx.send("I don't have permission to change nicknames.")

    @commands.command()
    async def nick(self, ctx, *, new_name: str = None):
        await self.change_nickname(ctx, new_name=new_name)

    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide the new nickname you want to set.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("An error occurred while processing your request.")
        else:
            await ctx.send("An error occurred.")


async def setup(bot):
    await bot.add_cog(WhoIs(bot))
    await bot.add_cog(TextToSpeech(bot))
    await bot.add_cog(ChangeNickname(bot))
