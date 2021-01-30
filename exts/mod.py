import discord
from discord.ext import commands
import typing
import aiosqlite

class Mod(commands.Cog, name="관리"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="경고")
    @commands.has_role(711753639722745896)
    async def _warn(ctx, member: discord.Member, *, reason: typing.Optional[str] = "사유가 지정되지 않음.")
        o = await aiosqlite.connect("Shark1ight.db")
        c = await o.cursor()
        await c.execute("INSERT INTO warns(user, admin, reason) VALUES('{member.id}', '{ctx.author.id}', '{reason}')")
        await o.commit()
        await o.close()
        await ctx.send(f"{member}에게 경고가 지급되었습니다. 사유 : *{reason}*")

def setup(bot):
    bot.add_cog(Mod(bot))
