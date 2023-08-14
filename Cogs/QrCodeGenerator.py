import io
import discord
from discord.ext import commands
from discord import File
import qrcode
import validators
import asyncio


class QrCodeGeneratorQuery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.QRCODE_API = "https://qrcode-monkey.p.rapidapi.com/qr/custom"

    async def generate_qrcode(self, bot, message: discord.Message, link: str):
        if message.author == bot.user:
            return

        if not validators.url(link):
            await message.channel.send("Invalid URL. Please provide a valid link.")
            return

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=5,
                border=4
            )

            qr.add_data(link)
            qr.make(fit=True)

            qr_img = qr.make_image(fill_color="black", back_color="white")

            # Save the QR code image to a BytesIO object
            img_io = io.BytesIO()
            qr_img.save(img_io)

            # Send the QR code image as a file attachment
            img_io.seek(0)  # Move the cursor to the beginning of the BytesIO object
            qr_file = File(img_io, filename="qrcode.png")

            await message.delete()
            await asyncio.sleep(1)
            await message.channel.send(file=qr_file)

        except Exception as e:
            await message.channel.send(f"An unexpected error occurred: {e}")

    @commands.command()
    async def qrcode(self, ctx, link: str):
        await self.generate_qrcode(ctx.bot, ctx.message, link)

    @qrcode.error
    async def qrcode_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: `!qrcode <link>`")
        else:
            await ctx.send(f"An error occurred: {error}")


async def setup(bot):
    await bot.add_cog(QrCodeGeneratorQuery(bot))
