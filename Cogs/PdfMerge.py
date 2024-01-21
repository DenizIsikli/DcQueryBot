import discord
from discord.ext import commands
from PyPDF2 import PdfFileReader, PdfFileWriter
import io
import aiohttp


class PDFMerge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def download_file(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return io.BytesIO(await response.read())

    @commands.command()
    async def pdfmerge(self, ctx):
        if len(ctx.message.attachments) < 2:
            await ctx.send("Please upload at least two PDF files.")
            return

        pdf_writer = PdfFileWriter()

        for attachment in ctx.message.attachments[:2]:
            if attachment.filename.endswith('.pdf'):
                file_stream = await self.download_file(attachment.url)
                pdf_reader = PdfFileReader(file_stream)
                for page in range(pdf_reader.getNumPages()):
                    pdf_writer.addPage(pdf_reader.getPage(page))

        merged_pdf_stream = io.BytesIO()
        pdf_writer.write(merged_pdf_stream)
        merged_pdf_stream.seek(0)

        await ctx.send(file=discord.File(merged_pdf_stream, 'Merged_Document.pdf'))


async def setup(bot):
    await bot.add_cog(PDFMerge(bot))
