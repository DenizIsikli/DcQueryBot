import os
import discord
from discord.ext import commands
import zlib


class FileCompression(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.input_file = None
        self.output_file = None

    @staticmethod
    async def compress_file(input_file, output_file):
        try:
            with open(input_file, 'rb') as f:
                data = f.read()
                compressed_data = zlib.compress(data, level=zlib.Z_BEST_COMPRESSION)

            with open(output_file, 'wb') as f:
                f.write(compressed_data)

            os.remove(input_file)
            os.remove(output_file)

        except FileNotFoundError:
            print(f'Error: The input file "{input_file}" was not found.')

        except Exception as e:
            print(f'An error occurred: {e}')

    @commands.command()
    async def compress(self, ctx):
        try:
            if len(ctx.message.attachments) == 0:
                await ctx.send("Please provide a file as an attachment.")
                return

            # Get the user's uploaded image
            image_attachment = ctx.message.attachments[0]

            self.input_file = f"tmp_{image_attachment.filename}"
            await image_attachment.save(self.input_file)

            self.output_file = f"tmp_{image_attachment.filename}.zlib"

            input_file_size = os.path.getsize(self.input_file)
            output_file_size = os.path.getsize(self.output_file)

            await self.compress_file(self.input_file, self.output_file)

            await ctx.send(f"Input file size (bytes): {input_file_size}\n"
                           f"Output file size (bytes): {output_file_size}\n")
            await ctx.send(file=discord.File(self.output_file))

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

        finally:
            if os.path.exists(self.input_file):
                os.remove(self.input_file)
            if os.path.exists(self.output_file):
                os.remove(self.output_file)


async def setup(bot):
    bot.add_cog(FileCompression(bot))
