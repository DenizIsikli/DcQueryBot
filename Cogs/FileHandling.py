import os
import discord
from discord.ext import commands
from fpdf import FPDF
import docx2pdf


class TextToPDF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def text_to_pdf(ctx, name: str = None):
        if not ctx.message.attachments:
            await ctx.send("You need to attach a text file to convert.")
            return

        file_attachment = ctx.message.attachments[0]

        if not name:
            name, _ = os.path.splitext(file_attachment.filename)

        if file_attachment.filename.lower().endswith(".txt"):
            content = await file_attachment.read()
            input_text = content.decode('utf-8')
            output_pdf = f"{name}.pdf"

            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, input_text)
            pdf.output(output_pdf)

            await ctx.message.delete()

            try:
                await ctx.send(file=discord.File(output_pdf))
            finally:
                os.remove(output_pdf)
        else:
            await ctx.send("Unsupported file format. Supported format: .txt")

    @commands.command()
    async def texttopdf(self, ctx, name: str = None):
        await self.text_to_pdf(ctx, name)


class WordToPDF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def word_to_pdf(ctx, name: str = None):
        if not ctx.message.attachments:
            await ctx.send("You need to attach a Word document to convert.")
            return

        file_attachment = ctx.message.attachments[0]

        if not name:
            name, _ = os.path.splitext(file_attachment.filename)

        if file_attachment.filename.lower().endswith(".docx") or file_attachment.filename.lower().endswith(".doc"):
            input_docx = f"{name}.docx"
            output_pdf = f"{name}.pdf"

            await file_attachment.save(input_docx)

            docx2pdf.convert(input_docx, output_pdf)

            await ctx.message.delete()

            try:
                await ctx.send(file=discord.File(output_pdf))
            finally:
                os.remove(output_pdf)
        else:
            await ctx.send("Unsupported file format. Supported format: .docx | .doc")

    @commands.command()
    async def wordtopdf(self, ctx, name: str = None):
        await self.word_to_pdf(ctx, name=name)


async def setup(bot):
    await bot.add_cog(TextToPDF(bot))
    await bot.add_cog(WordToPDF(bot))
