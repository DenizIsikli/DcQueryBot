from discord.ext import commands
import discord
from googletrans import Translator
from googletrans.constants import LANGUAGES
import os


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


def setup(bot):
    bot.add_cog(TranslateText(bot))
