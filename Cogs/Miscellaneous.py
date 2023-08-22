import os
import discord
from discord.ext import commands
import datetime
import aiohttp
import asyncio
from ibm_watson import TextToSpeechV1
from datetime import datetime
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class WhoIs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def who_is(ctx, member: discord.Member = None):
        try:
            if ctx.author == ctx.bot.user:
                return

            # If the member is not specified, the variable is then set to the author
            member = member or ctx.author

            embed = discord.Embed(
                title=f"Who is {member.display_name}",
                color=discord.Color.dark_theme()
            )

            embed.add_field(name="**ID:**", value=member.id)
            embed.add_field(name="**Name:**", value=member.display_name)

            embed.add_field(name="**Created Account On:**", value=member.created_at)
            embed.add_field(name="**Joined Server On:**", value=member.joined_at)

            roles = ', '.join(role.name for role in member.roles)
            embed.add_field(name="**Roles:**", value=roles)

            embed.add_field(name="**Highest Role:**", value=member.top_role)

            # Add & set footer with timestamp
            timestamp = datetime.utcnow()
            embed.timestamp = timestamp
            embed.set_footer(text=f"Requested by {ctx.author.name}")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):
        await self.who_is(ctx, member=member)

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

    @staticmethod
    async def cleanup(vc):
        if vc.is_connected():
            await vc.disconnect()
        os.remove("speech.mp3")

    async def text_to_speech(self, ctx, vc, *, text: str = None):
        try:
            if ctx.author == ctx.bot.user:
                return

            if ctx.author.voice and ctx.author.voice.channel:
                if text is not None and text.strip() != "":
                    response = self.client.synthesize(text, accept='audio/mp3')

                    # Save the audio to a file
                    with open("speech.mp3", "wb") as out_file:
                        out_file.write(response.get_result().content)

                    voice_channel = ctx.author.voice.channel
                    vc = await voice_channel.connect()

                    vc.play(discord.FFmpegPCMAudio("speech.mp3"), after=lambda error: self.cleanup(vc))

                    while vc.is_playing():
                        await asyncio.sleep(1)

                    await self.cleanup(vc)
                else:
                    await ctx.send("Please provide the text you want to convert to speech.")
            else:
                await ctx.send("You need to be inside a voice channel to use this command!")

        except Exception as e:
            await ctx.send(f"Failed to save the text to audio: {e}")
            await self.cleanup(vc)

    @commands.command()
    async def tts(self, ctx, *, text: str = None):
        voice_client = ctx.voice_client
        await self.text_to_speech(ctx, voice_client, text=text)

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
            if ctx.author == ctx.bot.user:
                return

            new_name_without_space = new_name.replace(" ", "_")
            old_name = ctx.author.display_name
            await ctx.author.edit(nick=new_name_without_space)
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


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = []

    @staticmethod
    async def reminder(ctx, duration: float = 0, *, reminder: str = None):
        if ctx.author == ctx.bot.user:
            return

        if duration <= 0:
            await ctx.send("Please provide a valid duration (in minutes) for the reminder.")
            return

        await asyncio.sleep(5)
        await ctx.message.delete()
        await asyncio.sleep(duration * 60)

        user_id = ctx.author
        await user_id.send(f"**Reminder**: {reminder}")

    @commands.command()
    async def remindme(self, ctx, duration: float = 0, *, reminder: str = None):
        if duration <= 0:
            await ctx.send("Please provide a valid duration (in minutes) for the reminder.")
            return

        if reminder is None:
            reminder = "Default reminder"

        await self.reminder(ctx, duration, reminder=reminder)

    @remindme.error
    async def reminder_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Please provide a valid duration.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: !remindme <duration in minutes> <reminder>")
        else:
            await ctx.send(f"An error occurred: {error}")


class GitHub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def bot_owner(ctx):
        await ctx.send("https://github.com/DenizIsikli")

    @commands.command()
    async def owner(self, ctx):
        await self.bot_owner(ctx)

    @staticmethod
    async def bot_picture(ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/826814606298316882/1142173434567200869/love.png")

    @commands.command()
    async def botpic(self, ctx):
        await self.bot_picture(ctx)

    @staticmethod
    async def bot_repository(ctx):
        await ctx.send("https://github.com/DenizIsikli/DcQueryBot")

    @commands.command()
    async def repo(self, ctx):
        await self.bot_repository(ctx)


async def setup(bot):
    await bot.add_cog(WhoIs(bot))
    await bot.add_cog(TextToSpeech(bot))
    await bot.add_cog(ChangeNickname(bot))
    await bot.add_cog(Reminder(bot))
    await bot.add_cog(GitHub(bot))
