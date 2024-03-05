import discord
from discord.ext import commands
import datetime


class HelpEmbedMain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def help_embed_main(ctx):
        if ctx.author == ctx.bot.user:
            return

        embed = discord.Embed(
            title="__Main Command List__",
            color=discord.Color.dark_theme()
        )
        embed.add_field(
            name="**!website**",
            value="Website for the Discord Bot",
            inline=False
        )
        embed.add_field(
            name="**!help1**",
            value="First command list",
        )
        embed.add_field(
            name="**!help2**",
            value="Second command list",
        )
        embed.add_field(
            name="**!help3**",
            value="Third command list",
        )
        embed.add_field(
            name="**!help4**",
            value="Fourth command list",
        )
        embed.add_field(
            name="**!help5**",
            value="Fifth command list",
        )
        embed.add_field(
            name="**!help6**",
            value="Sixth command list",
        )
        embed.add_field(
            name="**!help7**",
            value="Seventh command list",
        )
        embed.add_field(
            name="**!help8**",
            value="Eighth command list",
        )
        embed.add_field(
            name="**!admin**",
            value="Admin command list",
            inline=False
        )
        embed.add_field(
            name="**!commandlist**",
            value="Command list of all bot commands",
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        await self.help_embed_main(ctx)

    @help.error
    async def help_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


class HelpEmbed1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def help_embed_1(ctx):
        if ctx.author == ctx.bot.user:
            return

        embed = discord.Embed(
            title="__1st Command List__",
            color=discord.Color.dark_theme()
        )
        embed.add_field(
            name="**!urban**",
            value="Description: Retrieves a selection of 1-5 words from Urban Dictionary "
                  "that match the provided search query - word amount must be specified\n"
                  "!urban {int: word amount} {str: search query}\n"
                  "Example: *!urban Shookie* | *!urban 2 Shookie*",
            inline=False
        )
        embed.add_field(
            name="**!qrcode**",
            value="Description: Creates a Qr-Code based on the given link\n"
                  "!qrcode {str: link}\n"
                  "Example: *!qrcode GitHub.com*",
            inline=False
        )
        embed.add_field(
            name="**!imgur**",
            value="Description: Retrieves a random GIF from Imgur based on the specified category\n"
                  "!imgur {str: search query}\n"
                  "Example: *!imgur cat*",
            inline=False
        )
        embed.add_field(
            name="**!wiki**",
            value="Description: Retrieves a selection of 1-5 articles from Wikipedia "
                  "that match the provided search query - article amount must be specified\n"
                  "!wiki {int: article amount} {str: search query}\n"
                  "Example: *!wiki Lev Landau* | *!wiki 2 Lev Landau*",
            inline=False
        )
        embed.add_field(
            name="**!senti**",
            value="Description: Calculates the sentiment value of a Wikipedia article\n"
                  "!senti {str: link}\n"
                  "Example: *!senti `https://da.wikipedia.org/wiki/Lev_Landau`*",
            inline=False
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def help1(self, ctx):
        await self.help_embed_1(ctx)

    @help1.error
    async def help1_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


class HelpEmbed2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def help_embed_2(ctx):
        embed = discord.Embed(
            title="__2nd Command List__",
            color=discord.Color.dark_theme()
        )
        embed.add_field(
            name="**!mp3**",
            value="Description: Converts a YouTube video into a MP3 file based on the given link\n"
                  "!mp3 {str: link}\n"
                  "Example: *!mp3 `https://www.youtube.com/watch?v=HAZoLuME-PU`*",
            inline=False
        )
        embed.add_field(
            name="**!mp4**",
            value="Description: Converts a YouTube video into a MP4 file based on the given link\n"
                  "!mp4 {str: link}\n"
                  "Example: *!mp4 `https://www.youtube.com/watch?v=HAZoLuME-PU`*",
            inline=False
        )
        embed.add_field(
            name="**!ascii**",
            value="Description: Creates ASCII art based on the given text\n"
                  "!ascii {str: text}\n"
                  "Example: *!ascii placeholder*",
            inline=False

        )
        embed.add_field(
            name="**!asciicm**",
            value="Description: Creates ASCII art with CyberModule font based on the given text\n"
                  "!asciicm {str: text}\n"
                  "Example: *!asciicm placeholder*\n"
                  "`asciicm does not take numbers as an argument, only text`",
            inline=False
        )
        embed.add_field(
            name="**!gpt**",
            value="Description: Query ChatGPT with any given input\n"
                  "!gpt {str: content}\n"
                  "Example: *!gpt What is an API*\n",
            inline=False
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def help2(self, ctx):
        await self.help_embed_2(ctx)

    @help2.error
    async def help2_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


class HelpEmbed3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def help_embed_3(ctx):
        embed = discord.Embed(
            title="__3rd Command List__",
            color=discord.Color.dark_theme()
        )
        embed.add_field(
            name="**!tts**",
            value="Description: Text to speech based on the given text\n"
                  "!tts {str: text}\n"
                  "Example: *!tts Text to speech*\n",
            inline=False
        )
        embed.add_field(
            name="**!reminder**",
            value="Description: Places a reminder based on the given duration in minutes, and text\n"
                  "!reminder {float: duration} {str: reminder}\n"
                  "Example: *!reminder 25 Check the oven*\n",
            inline=False
        )
        embed.add_field(
            name="**!nickname**",
            value="Description: Changes your nickname on the server based on the given text\n"
                  "!nickname {str: text}\n"
                  "Example: *!nickname Bobby*\n",
            inline=False
        )
        embed.add_field(
            name="**!whois**",
            value="Description: Gives a thorough description of the person you @ - "
                  "No @ defaults to yourself\n"
                  "!whois {discord.Member: member}\n"
                  "Example: *!whois @Bobby* | *!whois*\n",
            inline=False
        )
        embed.add_field(
            name="**!resize**",
            value="Description: Resizes the image attachment based on the given dimensions\n"
                  "!resize {attachment: image} {int: width} {int: height}\n"
                  "Example: *!resize 300 150*\n",
            inline=False
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def help3(self, ctx):
        await self.help_embed_3(ctx)

    @help3.error
    async def help3_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


class HelpEmbed4(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def help_embed_4(ctx):
        embed = discord.Embed(
            title="__4th Command List__",
            color=discord.Color.dark_theme()
        )
        embed.add_field(
            name="**!blur**",
            value="Description: Applies a blur filter in the range of 1-5 to the given image\n"
                  "!blur {attachment: image} {float: blur_range}\n"
                  "Example: *!blur {image} {blur_range}*\n",
            inline=False
        )
        embed.add_field(
            name="**!sharpen**",
            value="Description: Applies a sharpen filter to the given image - "
                  "Choices: 'mild', 'medium', 'strong', 'extreme'\n"
                  "!sharpen {attachment: image} {str: sharpen_range}\n"
                  "Example: *!sharpen {image} {sharpen_range}*\n",
            inline=False
        )
        embed.add_field(
            name="**!sepia**",
            value="Description: Applies a vintage filter to the given image\n"
                  "!sepia {attachment: image}\n"
                  "Example: *!sepia {image}*\n",
            inline=False
        )
        embed.add_field(
            name="**!watercolor**",
            value="Description: Applies a watercolor filter to the given image\n"
                  "!watercolor {attachment: image}\n"
                  "Example: *!watercolor {image}*\n",
            inline=False
        )
        embed.add_field(
            name="**!grayscale**",
            value="Description: Applies a grayscale filter to the given image\n"
                  "!grayscale {attachment: image}\n"
                  "Example: *!grayscale {image}*\n",
            inline=False
        )
        embed.add_field(
            name="**!invert**",
            value="Description: Applies an invert filter to the given image\n"
                  "!invert {attachment: image}\n"
                  "Example: *!invert {image}*\n",
            inline=False
        )
        embed.add_field(
            name="**!solarize**",
            value="Description: Applies a solarize filter to the given image\n"
                  "!solarize {attachment: image}\n"
                  "Example: *!solarize {image}*\n",
            inline=False
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def help4(self, ctx):
        await self.help_embed_4(ctx)

    @help4.error
    async def help4_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


class HelpEmbed5(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def help_embed_5(ctx):
        embed = discord.Embed(
            title="__5th Command List__",
            color=discord.Color.dark_theme()
        )
        embed.add_field(
            name="**!anime**",
            value="Description: Returns an anime from MAL (My Anime List) based on the given name\n"
                  "!anime {str: anime}\n"
                  "Example: *!anime {anime}*\n",
            inline=False
        )
        embed.add_field(
            name="**!manga**",
            value="Description: Returns a manga from MAL (My Anime List) based on the given name\n"
                  "!manga {str: manga}\n"
                  "Example: *!manga {manga}*\n",
            inline=False
        )
        embed.add_field(
            name="**!steam**",
            value="Description: Returns a game from Steam based on the given name\n"
                  "!steam {str: game}\n"
                  "Example: *!steam {game}*\n",
            inline=False
        )
        embed.add_field(
            name="**!translate**",
            value="Description: Translates any given text to the target language - Use !languagecode if unsure\n"
                  "!translate {str: target_lang} {str: text}\n"
                  "Example: *!translate fr Hello*\n",
            inline=False
        )
        embed.add_field(
            name="**!languagecode**",
            value="Description: Shows a text file of the different language codes available for translation\n"
                  "!languagecode\n"
                  "Example: *!languagecode*\n",
            inline=False
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def help5(self, ctx):
        await self.help_embed_5(ctx)

    @help5.error
    async def help5_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


class HelpEmbed6(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def help_embed_6(ctx):
        embed = discord.Embed(
            title="__6th Command List__",
            color=discord.Color.dark_theme()
        )
        embed.add_field(
            name="**!texttopdf**",
            value="Description: Turns the given text file (.txt) into a PDF with a name of your choice\n"
                  "!texttopdf {str: name}\n"
                  "Example: *!texttopdf {attachment: .txt} {name}*\n",
            inline=False
        )
        embed.add_field(
            name="**!wordtopdf**",
            value="Description: Turns the given word file (.docx) into a PDF with a name of your choice\n"
                  "!wordtopdf {str: name}\n"
                  "Example: *!wordtopdf {attachment: .docx} {name}*\n",
            inline=False
        )
        embed.add_field(
            name="**!compress**",
            value="Description: Compresses any file\n"
                  "!compress {attachment: file}\n"
                  "Example: *!compress {attachment: .txt}*\n",
            inline=False
        )
        embed.add_field(
            name="**!decompress**",
            value="Description: Decompresses any file\n"
                  "!decompress {attachment: file}\n"
                  "Example: *!decompress {attachment: .txt}*\n",
            inline=False
        )
        embed.add_field(
            name="**!pomodoro**",
            value="Description: Starts a pomodoro timer with the given study duration, break duration and cycles\n"
                  "!pomodoro {float: study_duration} {float: break_duration} {int: cycles}\n"
                  "Example: *!pomodoro 25 5 4*\n",
            inline=False
        )
        embed.add_field(
            name="**!pomodorostop**",
            value="Description: Stops the pomodoro timer\n"
                  "!pomodorostop\n"
                  "Example: *!pomodorostop*\n",
            inline=False
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def help6(self, ctx):
        await self.help_embed_6(ctx)

    @help6.error
    async def help6_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


class HelpEmbed7(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def help_embed_7(ctx):
        embed = discord.Embed(
            title="__7th Command List__",
            color=discord.Color.dark_theme()
        )
        embed.add_field(
            name="**!callduration**",
            value="Description: Calculates the duration of your current voice call\n"
                  "!callduration\n"
                  "Example: *!callduration*\n",
            inline=False
        )
        embed.add_field(
            name="**!pdfmerge**",
            value="Description: Merges a maximum of 2 PDF files into one\n"
                  "!pdfmerge {attachment: pdf_file}\n"
                  "Example: *!pdfmerge {attachment: pdf_file}*\n",
            inline=False
        )
        embed.add_field(
            name="**!pricerunner**",
            value="Description: Retrieves a selection of 20 products from PriceRunner\n"
                  "!pricerunner {str: product name}\n"
                  "Example: *!pricerunner Intel Core i9*\n",
            inline=False
        )
        embed.add_field(
            name="**!serverinfo**",
            value="Description: Retrieves information about the server\n"
                  "!serverinfo\n"
                  "Example: *!serverinfo*\n",
            inline=False
        )
        embed.add_field(
            name="**!summyt**",
            value="Description: Summarizes a YouTube video using Summarize.tech\n"
                  "!summyt {attachment: youtube_url}\n"
                  "Example: *!summyt {attachment: youtube_url}*\n",
            inline=False
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def help7(self, ctx):
        await self.help_embed_7(ctx)

    @help7.error
    async def help7_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


class HelpEmbed8(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def help_embed_8(ctx):
        embed = discord.Embed(
            title="__8th Command List__",
            color=discord.Color.dark_theme()
        )
        embed.add_field(
            name="**!owner**",
            value="Description: Display the owner of the bot\n"
                  "!owner\n",
            inline=False
        )
        embed.add_field(
            name="**!botpic**",
            value="Description: Display the bots profile picture\n"
                  "!botpic\n",
            inline=False
        )
        embed.add_field(
            name="**!repo**",
            value="Description: Link to the bots repository\n"
                  "!repo\n",
            inline=False
        )
        embed.add_field(
            name="**!codeformat**",
            value="Description: Formats code based on the given language\n"
                  "Aliases: *cf*\n"
                  "!codeformat {str: language} {str: code}\n"
                  "Example: *!codeformat python print('Hello, World!')*\n",
            inline=False
        )
        embed.add_field(
            name="**!afk**",
            value="Description: Starts an AFK automation for the specified amount of seconds\n"
                  "(Type 'afkstop' to stop the timer) - Default = 60\n"
                  "!afk {int: timer}\n"
                  "Example: *!afk 60*\n",
            inline=False
        )

        # Add & set footer with timestamp
        timestamp = datetime.datetime.utcnow()
        embed.timestamp = timestamp
        embed.set_footer(text=f"Requested by {ctx.author.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def help8(self, ctx):
        await self.help_embed_8(ctx)

    @help8.error
    async def help8_error(self, ctx):
        await ctx.send("An error occurred while processing your request.")


async def setup(bot):
    await bot.add_cog(HelpEmbedMain(bot))
    await bot.add_cog(HelpEmbed1(bot))
    await bot.add_cog(HelpEmbed2(bot))
    await bot.add_cog(HelpEmbed3(bot))
    await bot.add_cog(HelpEmbed4(bot))
    await bot.add_cog(HelpEmbed5(bot))
    await bot.add_cog(HelpEmbed6(bot))
    await bot.add_cog(HelpEmbed7(bot))
    await bot.add_cog(HelpEmbed8(bot))
