import io
import asyncio
import discord
from discord.ext import commands
from PIL import Image, ImageFilter


class ImageManipulation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def apply_blur(ctx, blur_range: float = 1.0):
        try:
            # Get the user's uploaded image
            image_attachment = ctx.message.attachments[0]

            # Read the attachment as bytes
            image_bytes = await image_attachment.read()

            # Open the image using PIL
            image = Image.open(io.BytesIO(image_bytes))

            # Parameters:
            # - range(optional): Amount of blur(0.1 to 5.0, default: 1.0)
            if blur_range < 0.1 or blur_range > 5.0:
                await ctx.send("Please provide a range from 0.1 to 5.0.")
                return

            filtered_image = image.filter(ImageFilter.GaussianBlur(radius=blur_range))

            # Convert the PIL Image to bytes since discord.File doesn't take "Image"
            img_byte_array = io.BytesIO()
            filtered_image.save(img_byte_array, format="PNG")

            # Seek back to the beginning of the buffer
            img_byte_array.seek(0)

            await ctx.message.delete()
            await asyncio.sleep(0.2)
            await ctx.send(file=discord.File(img_byte_array, "BlurredFilter_image.png"))

        except IndexError:
            await ctx.send("Please provide an image as an attachment.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def blur(self, ctx, blur_range: float = 1.0):
        await self.apply_blur(ctx, blur_range)

    @blur.error
    async def blur_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Please provide a valid blur range.")
        else:
            await ctx.send(f"An error occurred: {error}")

    @staticmethod
    async def apply_sharpen(ctx, sharpen_range: str = None):
        try:
            image_attachment = ctx.message.attachments[0]

            # Read the attachment as bytes
            image_bytes = await image_attachment.read()

            # Open the image using PIL
            image = Image.open(io.BytesIO(image_bytes))

            # Range: mild, medium, strong
            sharpness_switch = {
                "mild": lambda: image.filter(ImageFilter.UnsharpMask(radius=2, percent=50)),
                "medium": lambda: image.filter(ImageFilter.UnsharpMask(radius=2, percent=100)),
                "strong": lambda: image.filter(ImageFilter.UnsharpMask(radius=2, percent=150)),
                "extreme": lambda: image.filter(ImageFilter.UnsharpMask(radius=4, percent=250))
            }

            filtered_image = None  # Initialize with a default value
            filtered_image_function = sharpness_switch.get(sharpen_range)
            if filtered_image_function:
                filtered_image = filtered_image_function()
            else:
                await ctx.send("Invalid sharpening range - Choose: 'mild', 'medium', 'strong', or 'extreme'.")

            # Convert the PIL Image to bytes since discord.File doesn't take "Image"
            img_byte_array = io.BytesIO()
            filtered_image.save(img_byte_array, format="PNG")

            # Seek back to the beginning of the buffer
            img_byte_array.seek(0)

            await ctx.message.delete()
            await asyncio.sleep(0.2)
            await ctx.send(file=discord.File(img_byte_array, "SharpenFilter_image.png"))

        except IndexError:
            await ctx.send("Please provide an image as an attachment.")

    @commands.command()
    async def sharpen(self, ctx, sharpen_range: str = None):
        await self.apply_sharpen(ctx, sharpen_range)

    @sharpen.error
    async def sharpen_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Please provide a valid blur range.")


async def setup(bot):
    await bot.add_cog(ImageManipulation(bot))
