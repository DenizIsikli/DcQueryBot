import io
import discord
from discord.ext import commands
from PIL import Image, ImageFilter


class ImageManipulation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def apply_blur(ctx):
        try:
            # Get the user's uploaded image
            image = ctx.message.attachments[0]

            # Open the image using PIL
            image = Image.open(image.fp)
            filtered_image = image.filter(ImageFilter.BLUR)

            # Convert the PIL Image to bytes since discord.File doesn't take "Image"
            img_byte_array = io.BytesIO()
            filtered_image.save(img_byte_array, format="PNG")

            # Send the filtered image
            await ctx.send(file=discord.File(img_byte_array, "BlurredFilter_image.png"))

        except IndexError:
            await ctx.send("Please provide an image as an attachment.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @staticmethod
    async def apply_sharpen(ctx):
        try:
            image = ctx.message.attachments[0]

            # Open the image using PIL
            image = Image.open(image.fp)
            filtered_image = image.filter(ImageFilter.SHARPEN)

            # Convert the PIL Image to bytes since discord.File doesn't take "Image"
            img_byte_array = io.BytesIO()
            filtered_image.save(img_byte_array, format="PNG")

            # Send the filtered image
            await ctx.send(file=discord.File(img_byte_array, "SharpenFilter_image.png"))

        except IndexError:
            await ctx.send("Please provide an image as an attachment.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(ImageManipulation(bot))
