import discord
from discord.ext import commands
import config

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("상어 "),
    help_command=None,
    intents=discord.Intents.all()
    chunk_guilds_at_startup=True,
    description="Developers Forum 관리하는 봇"
)
def startup(bot):
    exts = [
        "jishaku",
        "exts.mod",
        "exts.auto",
        "exts.event"
    ]
    for ext in exts:
        try:
            bot.load_extension(ext)
        except Exception as e:
            print(f"{ext} Failed - {e}")
        else:
            print(f"{ext} Loaded")








startup(bot)
bot.run(config.Token)
