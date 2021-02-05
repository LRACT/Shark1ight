import discord
from discord.ext import commands
import aiosqlite

class Automatic(commands.Cog, name="자동 응답기"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="추가")
    async def _add(self, ctx, word, *, reply):
        o = await aiosqlite.connect("Shark1ight.sqlite")
        c = await o.cursor()
        await c.execute(f"SELECT * FROM cc WHERE word = '{word}'")
        rows = await c.fetchall()
        if not rows:
            await c.execute(f"INSERT INTO cc(word, reply, lock, author) VALUES('{word}', '{reply}', 'false', '{ctx.author.id}')")
            await o.commit()
            await ctx.send(f"")
        else:
            raise commands.BadArgument
        await o.close()

def setup(bot):
    bot.add_cog(Automatic(bot))