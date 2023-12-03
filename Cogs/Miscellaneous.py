import os
import io
import asyncio
import discord
import datetime
from PIL import Image
from datetime import datetime
from discord.ext import commands
from googletrans import Translator
from googletrans.constants import LANGUAGES


class WhoIs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def who_is(ctx, member: discord.Member = None):
        try:
            if ctx.author == ctx.bot.user:
                return

            # If the member is not specified, the variable is then set to the author
            member = member or ctx.author

            embed = discord.Embed(
                title=f"Who is {member.display_name}",
                color=discord.Color.dark_theme()
            )

            embed.add_field(name="**ID:**", value=member.id)
            embed.add_field(name="**Name:**", value=member.display_name)

            embed.add_field(name="**Created Account On:**", value=member.created_at)
            embed.add_field(name="**Joined Server On:**", value=member.joined_at)

            roles = ', '.join(role.name for role in member.roles)
            embed.add_field(name="**Roles:**", value=roles)

            embed.add_field(name="**Highest Role:**", value=member.top_role)

            # Add & set footer with timestamp
            timestamp = datetime.utcnow()
            embed.timestamp = timestamp
            embed.set_footer(text=f"Requested by {ctx.author.name}")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def whois(self, ctx, member: discord.Member = None):
        await self.who_is(ctx, member=member)

    @whois.error
    async def whois_error(self, ctx, error):
        if isinstance(error, commands.UserNotFound):
            await ctx.send("User not found. Please provide a valid user mention or ID.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad argument. Please provide a valid user mention or ID.")
        else:
            await ctx.send("An error occurred while processing your request.")


class ChangeNickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def change_nickname(ctx, *, new_name: str = None):
        try:
            if ctx.author == ctx.bot.user:
                return

            new_name_without_space = new_name.replace(" ", "_")
            old_name = ctx.author.display_name
            await ctx.author.edit(nick=new_name_without_space)
            await ctx.send(f"Nickname changed from {old_name} to {new_name}")

        except discord.Forbidden:
            await ctx.send("I don't have permission to change nicknames.")

    @commands.command()
    async def nickname(self, ctx, *, new_name: str = None):
        await self.change_nickname(ctx, new_name=new_name)

    @nickname.error
    async def nickname_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please provide the new nickname you want to set.")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("An error occurred while processing your request.")
        else:
            await ctx.send("An error occurred.")


class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = []

    @staticmethod
    async def reminder(ctx, duration: float = 1, *, reminder: str = None):
        if ctx.author == ctx.bot.user:
            return

        if duration <= 0:
            await ctx.send("Please provide a valid duration (in minutes) for the reminder.")
            return

        await asyncio.sleep(3)
        await ctx.message.delete()
        await asyncio.sleep(duration * 60)

        await ctx.author.send(f"**Reminder**: {reminder}")

    @commands.command()
    async def remindme(self, ctx, duration: float = 0, *, reminder: str = None):
        if duration <= 0:
            await ctx.send("Please provide a valid duration (in minutes) for the reminder.")
            return

        if reminder is None:
            reminder = "Default reminder"

        await self.reminder(ctx, duration, reminder=reminder)

    @remindme.error
    async def reminder_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid argument. Please provide a valid duration.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Usage: !remindme <duration in minutes> <reminder>")
        else:
            await ctx.send(f"An error occurred: {error}")


class ResizeImage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def resize_image(ctx, width: int = None, height: int = None):
        if ctx.author == ctx.bot.user:
            return

        if width is None or height is None:
            await ctx.send("You need to specify the dimensions you want.")
            return

        image_size = (width, height)

        image_attachment = ctx.message.attachments[0]
        image_bytes = await image_attachment.read()

        try:
            image = Image.open(io.BytesIO(image_bytes))
            resized_image = image.resize(image_size)

            resized_image_bytes = io.BytesIO()
            resized_image.save(resized_image_bytes, format="PNG")
            resized_image_bytes.seek(0)

            await ctx.message.delete()
            await asyncio.sleep(0.2)
            await ctx.send(file=discord.File(resized_image_bytes, "Resized_Image.png"))
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def resize(self, ctx, width: int = None, height: int = None):
        await self.resize_image(ctx, width, height)


class TranslateText(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()

        self.count = 0

    async def translater(self, ctx, target_lang: str = None, *, text: str = None):
        if ctx.author == ctx.bot.user:
            return

        if target_lang is None:
            await ctx.send("Specify a language.")
            return

        if text is None:
            await ctx.send("Specify text to translate.")
            return

        try:
            if target_lang in LANGUAGES:
                translation = self.translator.translate(text, dest=target_lang)
                await ctx.send(f"Translation to {LANGUAGES[target_lang]}: {translation.text}")
            else:
                await ctx.send("Invalid target language. Please provide a valid language code: !languagecode")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def translate(self, ctx, target_lang: str = None, *, text: str = None):
        await self.translater(ctx, target_lang, text=text)

    @commands.command()
    async def languagecode(self, ctx):
        with open("Language_Codes.txt", "w") as file:
            file.write(
                "Language Codes\n"
                "af: Afrikaans | sq: Albanian | am: Amharic | ar: Arabic | hy: Armenian\n"
                "az: Azerbaijani | eu: Basque | be: Belarusian | bn: Bengali | bs: Bosnian\n"
                "bg: Bulgarian | ca: Catalan | ceb: Cebuano | ny: Chichewa | zh-cn: Chinese (Simplified)\n"
                "zh-tw: Chinese (Traditional) | co: Corsican | hr: Croatian | cs: Czech | da: Danish\n"
                "nl: Dutch | en: English | eo: Esperanto | et: Estonian | tl: Filipino\n"
                "fi: Finnish | fr: French | fy: Frisian | gl: Galician | ka: Georgian\n"
                "de: German | el: Greek | gu: Gujarati | ht: Haitian Creole | ha: Hausa\n"
                "haw: Hawaiian | iw: Hebrew | he: Hebrew | hi: Hindi | hmn: Hmong\n"
                "hu: Hungarian | is: Icelandic | ig: Igbo | id: Indonesian | ga: Irish\n"
                "it: Italian | ja: Japanese | jw: Javanese | kn: Kannada | kk: Kazakh\n"
                "km: Khmer | ko: Korean | ku: Kurdish (Kurmanji) | ky: Kyrgyz | lo: Lao\n"
                "la: Latin | lv: Latvian | lt: Lithuanian | lb: Luxembourgish | mk: Macedonian\n"
                "mg: Malagasy | ms: Malay | ml: Malayalam | mt: Maltese | mi: Maori\n"
                "mr: Marathi | mn: Mongolian | my: Myanmar (Burmese) | ne: Nepali | no: Norwegian\n"
                "or: Odia | ps: Pashto | fa: Persian | pl: Polish | pt: Portuguese\n"
                "pa: Punjabi | ro: Romanian | ru: Russian | sm: Samoan | gd: Scots Gaelic\n"
                "sr: Serbian | st: Sesotho | sn: Shona | sd: Sindhi | si: Sinhala\n"
                "sk: Slovak | sl: Slovenian | so: Somali | es: Spanish | su: Sundanese\n"
                "sw: Swahili | sv: Swedish | tg: Tajik | ta: Tamil | te: Telugu\n"
                "th: Thai | tr: Turkish | uk: Ukrainian | ur: Urdu | ug: Uyghur\n"
                "uz: Uzbek | vi: Vietnamese | cy: Welsh | xh: Xhosa | yi: Yiddish\n"
                "yo: Yoruba | zu: Zulu\n"
            )

        await ctx.send(file=discord.File("Language_Codes.txt"))
        os.remove("Language_Codes.txt")


class GitHub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def bot_owner(ctx):
        await ctx.send("https://github.com/DenizIsikli")

    @commands.command()
    async def owner(self, ctx):
        await self.bot_owner(ctx)

    @staticmethod
    async def bot_picture(ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/826814606298316882/1142173434567200869/love.png")

    @commands.command()
    async def botpic(self, ctx):
        await self.bot_picture(ctx)

    @staticmethod
    async def bot_repository(ctx):
        await ctx.send("https://github.com/DenizIsikli/DcQueryBot")

    @commands.command()
    async def repo(self, ctx):
        await self.bot_repository(ctx)


class CommandList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_list_file = "C:\\Users\\deniz\\PycharmProjects\\DcQueryBot\\CommandList.txt"

    @commands.command(name="commandlist")
    async def command_list(self, ctx):
        try:
            await ctx.send(file=discord.File(self.command_list_file))
        except FileNotFoundError:
            await ctx.send("Command list not found.")
        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")


async def setup(bot):
    await bot.add_cog(WhoIs(bot))
    await bot.add_cog(ChangeNickname(bot))
    await bot.add_cog(Reminder(bot))
    await bot.add_cog(ResizeImage(bot))
    await bot.add_cog(TranslateText(bot))
    await bot.add_cog(GitHub(bot))
    await bot.add_cog(CommandList(bot))
