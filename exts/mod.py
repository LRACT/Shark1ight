import discord
from discord.ext import commands
import typing

class Mod(commands.Cog, name="관리"):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Mod(bot))
