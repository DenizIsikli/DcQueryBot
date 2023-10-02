import io
import asyncio
import discord
from discord.ext import commands
from PIL import Image, ImageFilter, ImageOps, ImageChops


class ApplyBlur(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def apply_blur(ctx, blur_range: float = 1.0):
        try:
            if ctx.author == ctx.bot.user:
                return

            # Get the user's uploaded image
            image_attachment = ctx.message.attachments[0]

            if image_attachment is None:
                await ctx.send("Please provide an image as an attachment.")
                return

            # Read the attachment as bytes
            image_bytes = await image_attachment.read()

            # Open the image using PIL
            image = Image.open(io.BytesIO(image_bytes))

            # Parameters:
            # - range(optional): Amount of blur(0.1 to 5.0, default: 1.0)
            if blur_range < 0.1 or blur_range > 5.0:
                await ctx.send("Please provide a range from 0.1 to 5.0.")
                return

            blur_image = image.filter(ImageFilter.GaussianBlur(radius=blur_range))

            # Convert the PIL Image to bytes since discord.File doesn't take "Image"
            img_byte_array = io.BytesIO()
            blur_image.save(img_byte_array, format="PNG")

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


class ApplySharpen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def apply_sharpen(ctx, sharpen_range: str = "medium"):
        try:
            if ctx.author == ctx.bot.user:
                return

            image_attachment = ctx.message.attachments[0]

            if image_attachment is None:
                await ctx.send("Please provide an image as an attachment.")
                return

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

            sharp_image = None  # Initialize with a default value
            filtered_image_function = sharpness_switch.get(sharpen_range)
            if filtered_image_function:
                sharp_image = filtered_image_function()
            else:
                await ctx.send("Invalid sharpening range - Choose: 'mild', 'medium', 'strong', or 'extreme'.")

            # Convert the PIL Image to bytes since discord.File doesn't take "Image"
            img_byte_array = io.BytesIO()
            sharp_image.save(img_byte_array, format="PNG")

            # Seek back to the beginning of the buffer
            img_byte_array.seek(0)

            await ctx.message.delete()
            await asyncio.sleep(0.2)
            await ctx.send(file=discord.File(img_byte_array, "SharpenFilter_image.png"))

        except IndexError:
            await ctx.send("Please provide an image as an attachment.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def sharpen(self, ctx, sharpen_range: str = "medium"):
        await self.apply_sharpen(ctx, sharpen_range)

    @sharpen.error
    async def sharpen_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Please provide a valid blur range.")


class ApplySepia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def apply_sepia(ctx):
        try:
            if ctx.author == ctx.bot.user:
                return

            image_attachment = ctx.message.attachments[0]

            if image_attachment is None:
                await ctx.send("Please provide an image as an attachment.")
                return

            # Read the attachment as bytes
            image_bytes = await image_attachment.read()

            # Open the image using PIL
            image = Image.open(io.BytesIO(image_bytes))

            # Apply sepia filter
            sepia_image = ImageOps.colorize(image.convert("L"), "#704214", "#FFDAA4")

            # Convert the PIL Image to bytes
            img_byte_array = io.BytesIO()
            sepia_image.save(img_byte_array, format="PNG")

            # Seek back to the beginning of the buffer
            img_byte_array.seek(0)

            await ctx.message.delete()
            await asyncio.sleep(0.2)
            await ctx.send(file=discord.File(img_byte_array, "SepiaFilter_image.png"))

        except IndexError:
            await ctx.send("Please provide an image as an attachment.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def sepia(self, ctx):
        await self.apply_sepia(ctx)

    @sepia.error
    async def sepia_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Please provide a valid image.")


class ApplyWatercolor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def apply_watercolor(ctx):
        try:
            if ctx.author == ctx.bot.user:
                return

            image_attachment = ctx.message.attachments[0]

            if image_attachment is None:
                await ctx.send("Please provide an image as an attachment.")
                return

            # Read the attachment as bytes
            image_bytes = await image_attachment.read()

            # Open the image using PIL
            image = Image.open(io.BytesIO(image_bytes))

            # Apply a Gaussian blur for softening
            blurred_image = image.filter(ImageFilter.GaussianBlur(radius=10))

            # Blend the original image and the blurred version using "lighter"
            watercolor_image = ImageChops.lighter(image, blurred_image)

            # Convert the PIL Image to bytes
            img_byte_array = io.BytesIO()
            watercolor_image.save(img_byte_array, format="PNG")

            # Seek back to the beginning of the buffer
            img_byte_array.seek(0)

            await ctx.message.delete()
            await asyncio.sleep(0.2)
            await ctx.send(file=discord.File(img_byte_array, "WatercolorFilter_image.png"))

        except IndexError:
            await ctx.send("Please provide an image as an attachment.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def watercolor(self, ctx):
        await self.apply_watercolor(ctx)

    @watercolor.error
    async def watercolor_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Please provide a valid image.")


class ApplyGrayscale(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def apply_grayscale(ctx):
        try:
            if ctx.author == ctx.bot.user:
                return

            image_attachment = ctx.message.attachments[0]

            if image_attachment is None:
                await ctx.send("Please provide an image as an attachment.")
                return

            # Read the attachment as bytes
            image_bytes = await image_attachment.read()

            # Open the image using PIL
            image = Image.open(io.BytesIO(image_bytes))

            # Convert the image to grayscale
            grayscale_image = image.convert("L")

            # Convert the PIL Image to bytes since discord.File doesn't take "Image"
            img_byte_array = io.BytesIO()
            grayscale_image.save(img_byte_array, format="PNG")

            # Seek back to the beginning of the buffer
            img_byte_array.seek(0)

            await ctx.message.delete()
            await asyncio.sleep(0.2)
            await ctx.send(file=discord.File(img_byte_array, "GrayscaleFilter_image.png"))

        except IndexError:
            await ctx.send("Please provide an image as an attachment.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def grayscale(self, ctx):
        await self.apply_grayscale(ctx)

    @grayscale.error
    async def grayscale_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument.")
        else:
            await ctx.send(f"An error occurred: {error}")


class ApplyInvert(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def apply_invert(ctx):
        try:
            if ctx.author == ctx.bot.user:
                return

            image_attachment = ctx.message.attachments[0]

            if image_attachment is None:
                await ctx.send("Please provide an image as an attachment.")
                return

            # Read the attachment as bytes
            image_bytes = await image_attachment.read()

            # Open the image using PIL
            image = Image.open(io.BytesIO(image_bytes))

            # Invert the image
            inverted_image = ImageOps.invert(image)

            # Convert the PIL Image to bytes since discord.File doesn't take "Image"
            img_byte_array = io.BytesIO()
            inverted_image.save(img_byte_array, format="PNG")

            # Seek back to the beginning of the buffer
            img_byte_array.seek(0)

            await ctx.message.delete()
            await asyncio.sleep(0.2)
            await ctx.send(file=discord.File(img_byte_array, "InvertedFilter_image.png"))

        except IndexError:
            await ctx.send("Please provide an image as an attachment.")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def invert(self, ctx):
        await self.apply_invert(ctx)

    @invert.error
    async def invert_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument.")
        else:
            await ctx.send(f"An error occurred: {error}")


async def setup(bot):
    await bot.add_cog(ApplyBlur(bot))
    await bot.add_cog(ApplySharpen(bot))
    await bot.add_cog(ApplySepia(bot))
    await bot.add_cog(ApplyWatercolor(bot))
    await bot.add_cog(ApplyGrayscale(bot))
    await bot.add_cog(ApplyInvert(bot))
