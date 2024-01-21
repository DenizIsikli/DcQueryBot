import io
import asyncio
import discord
import datetime
from PIL import Image
from datetime import datetime
from discord.ext import commands


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
    async def nickname(self, ctx, *, new_name: str = None):
        await self.change_nickname(ctx, new_name=new_name)

    @nickname.error
    async def nickname_error(self, ctx, error):
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
    async def reminder(ctx, duration: float, *, reminder: str):
        if ctx.author == ctx.bot.user:
            return

        if duration <= 0:
            await ctx.send("Please provide a valid duration (in minutes) for the reminder.")
            return

        await asyncio.sleep(3)
        await ctx.message.delete()
        await asyncio.sleep(duration * 60)

        await ctx.author.send(f"**Reminder**: {reminder}")

    @commands.command()
    async def remindme(self, ctx, duration: float = 10, *, reminder: str = None):
        if duration <= 0:
            await ctx.send("Please provide a valid duration (in minutes) for the reminder.")
            return

        if reminder is None:
            reminder = "No reminder was specified"

        await self.reminder(ctx, duration, reminder=reminder)

    @remindme.error
    async def reminder_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Please provide a valid duration.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: !remindme <duration in minutes> <reminder>")
        else:
            await ctx.send(f"An error occurred: {error}")


class ResizeImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def resize_image(ctx, width: int = None, height: int = None):
        if ctx.author == ctx.bot.user:
            return

        if width is None or height is None:
            await ctx.send("You need to specify the dimensions you want.")
            return

        image_size = (width, height)

        image_attachment = ctx.message.attachments[0]
        image_bytes = await image_attachment.read()

        try:
            image = Image.open(io.BytesIO(image_bytes))
            resized_image = image.resize(image_size)

            resized_image_bytes = io.BytesIO()
            resized_image.save(resized_image_bytes, format="PNG")
            resized_image_bytes.seek(0)

            await ctx.message.delete()
            await asyncio.sleep(0.2)
            await ctx.send(file=discord.File(resized_image_bytes, "Resized_Image.png"))
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def resize(self, ctx, width: int = None, height: int = None):
        await self.resize_image(ctx, width, height)


class CommandList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_list_file = "C:\\Users\\deniz\\PycharmProjects\\DcQueryBot\\CommandList.txt"

    @commands.command(name="commandlist")
    async def command_list(self, ctx):
        try:
            await ctx.send(file=discord.File(self.command_list_file))
        except FileNotFoundError:
            await ctx.send("Command list not found.")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")


async def setup(bot):
    await bot.add_cog(WhoIs(bot))
    await bot.add_cog(ChangeNickname(bot))
    await bot.add_cog(Reminder(bot))
    await bot.add_cog(ResizeImage(bot))
    await bot.add_cog(GitHub(bot))
    await bot.add_cog(CommandList(bot))
