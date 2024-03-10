import io
import os
import asyncio
import discord
from PIL import Image
from discord.ext import commands
from dotenv import load_dotenv


class ChangeNickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def change_nickname(ctx, *, new_name: str = None):
        try:
            if ctx.author == ctx.bot.user:
                return

            if new_name is None:
                await ctx.send("Please provide the new nickname you want to set.")
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

        if len(ctx.message.attachments) == 0:
            await ctx.send("You need to attach an image to resize.")
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

    @commands.command(aliases=["rimg"])
    async def resize(self, ctx, width: int = None, height: int = None):
        await self.resize_image(ctx, width, height)


class CommandList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_dir = "../config/config.env"
        load_dotenv(self.base_dir, verbose=True)
        self.command_list_file = os.getenv("COMMAND_LIST_PATH")

    @commands.command(aliases=["cmdl"])
    async def commandlist(self, ctx):
        try:
            await ctx.send(file=discord.File(self.command_list_file))
        except FileNotFoundError:
            await ctx.send("Command list not found.")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")


async def setup(bot):
    await bot.add_cog(ChangeNickname(bot))
    await bot.add_cog(ResizeImage(bot))
    await bot.add_cog(CommandList(bot))
