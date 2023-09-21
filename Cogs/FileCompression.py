import io
import os
import discord
from discord.ext import commands
import zlib


class FileCompression(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def compress_file(ctx, input_file=None, output_file=None):
        try:
            with open(input_file, 'rb') as f:
                data = f.read()
                compressed_data = zlib.compress(data, level=zlib.Z_BEST_COMPRESSION)

            with open(output_file, 'wb') as f:
                f.write(compressed_data)

            return output_file

        except FileNotFoundError:
            await ctx.send(f'Error: The input file "{input_file}" was not found.')

        except Exception as e:
            await ctx.send(f'An error occurred: {e}')

    @commands.command()
    async def compress(self, ctx):
        try:
            if len(ctx.message.attachments) == 0:
                await ctx.send("Please provide a file as an attachment.")
                return

            # Get the user's uploaded file
            file_attachment = ctx.message.attachments[0]
            input_file = f"tmp_{file_attachment.filename}"
            await file_attachment.save(input_file)

            output_file = f"tmp_{os.path.splitext(input_file)[0]}.zlib"
            compressed_output = await self.compress_file(ctx, input_file, output_file)

            input_file_size = os.path.getsize(input_file)
            output_file_size = os.path.getsize(compressed_output)

            if compressed_output:
                await ctx.message.delete()
                await ctx.send(f"Input file size (bytes): {input_file_size}\n"
                               f"Output file size (bytes): {output_file_size}\n")
                await ctx.send(file=discord.File(compressed_output))

                os.remove(input_file)
                os.remove(compressed_output)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(FileCompression(bot))
