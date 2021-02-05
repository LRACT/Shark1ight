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
            await o.close()
            await ctx.send(f"<:cs_yes:659355468715786262> {ctx.author.mention} - `{word}` 단어를 추가했어요.")
        else:
            await o.close()
            raise commands.BadArgument
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            o = await aiosqlite.connect("Shark1ight.sqlite")
            c = await o.cursor()
            name = ctx.message.content.split(" ")[1]
            await c.execute(f"SELECT * FROM cc WHERE word = '{name}'")
            rows = await c.fetchall()
            if rows:
                user = self.bot.get_user(int(rows[0][3]))
                await ctx.send(f"{rows[0][1]}\n \nMade by `{user}`")
            await o.close()

def setup(bot):
    bot.add_cog(Automatic(bot))