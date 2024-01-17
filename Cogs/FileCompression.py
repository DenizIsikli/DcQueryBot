import asyncio
import os
import discord
from discord.ext import commands
import zlib
import base64


class FileCompression(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def compress_file(ctx, input_file=None, output_file=None):
        try:
            with open(input_file, 'rb') as f:
                data = f.read()
                compressed_data = zlib.compress(data, level=zlib.Z_BEST_COMPRESSION)
                b64_encoded_data = base64.b64encode(compressed_data)

            with open(output_file, 'w') as f:
                f.write(b64_encoded_data.decode('utf-8'))

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
            file_extension = os.path.splitext(file_attachment.filename)[1][1:]

            input_file = f"{file_attachment.filename}"
            await file_attachment.save(input_file)

            output_file = f"Compressed_{os.path.splitext(input_file)[0]}.{file_extension}"
            compressed_output = await self.compress_file(ctx, input_file, output_file)

            input_file_size = os.path.getsize(input_file)
            output_file_size = os.path.getsize(compressed_output)

            if compressed_output:
                await asyncio.sleep(1)
                await ctx.message.delete()
                await ctx.send(f"Input file size (bytes): {input_file_size}\n"
                               f"Output file size (bytes): {output_file_size}\n")
                await ctx.send(file=discord.File(compressed_output))

                os.remove(input_file)
                os.remove(compressed_output)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @staticmethod
    async def decompress_file(ctx, input_file=None, output_file=None):
        try:
            with open(input_file, 'r') as f:
                b64_encoded_data = f.read()
                compressed_data = base64.b64decode(b64_encoded_data)
                decompressed_data = zlib.decompress(compressed_data)

            with open(output_file, 'wb') as f:
                f.write(decompressed_data)

            return output_file

        except FileNotFoundError:
            await ctx.send(f'Error: The input file "{input_file}" was not found.')

        except Exception as e:
            await ctx.send(f'An error occurred: {e}')

    @commands.command()
    async def decompress(self, ctx):
        try:
            if len(ctx.message.attachments) == 0:
                await ctx.send("Please provide a file as an attachment.")
                return

            # Get the user's uploaded file
            file_attachment = ctx.message.attachments[0]
            file_extension = os.path.splitext(file_attachment.filename)[1][1:]

            input_file = f"{file_attachment.filename}"
            await file_attachment.save(input_file)

            output_file = f"Decompressed_{os.path.splitext(input_file)[0]}.{file_extension}"
            decompressed_output = await self.decompress_file(ctx, input_file, output_file)

            input_file_size = os.path.getsize(input_file)
            output_file_size = os.path.getsize(decompressed_output)

            if decompressed_output:
                await asyncio.sleep(1)
                await ctx.message.delete()
                await ctx.send(f"Input file size (bytes): {input_file_size}\n"
                               f"Output file size (bytes): {output_file_size}\n")
                await ctx.send(file=discord.File(decompressed_output))

                os.remove(input_file)
                os.remove(decompressed_output)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")


async def setup(bot):
    await bot.add_cog(FileCompression(bot))
