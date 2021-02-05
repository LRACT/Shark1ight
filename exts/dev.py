import discord
from discord.ext import commands
import aiosqlite

class Developers(commands.Cog, name="봇 관리용"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="DB")
    @commands.is_owner()
    async def _database(self, ctx, todo, *, command):
        o = await aiosqlite.connect("Shark1ight.sqlite")
        c = await o.cursor()
        if todo == "commit":
            await c.execute(command)
            await o.commit()
            await o.close()
            await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
        elif todo == "fetch":
            await c.execute(command)
            a = ""
            rows = await c.fetchall()
            for row in rows:
                a += f"{row}\n"
            if len(a) <= 2000:
                await ctx.send(a)
            else:
                print(a)
                await ctx.send(a[:2000])
            await o.close()
            await ctx.message.add_reaction("<:cs_yes:659355468715786262>")
        else:
            await o.close()
            raise commands.BadArgument
    
    @commands.command(name="등록")
    @commands.has_role(711753639722745896)
    async def _register(self, ctx, bot: discord.Member, owner: discord.Member):
        if bot.bot == True and owner.bot == False:
            o = await aiosqlite.connect("Shark1ight.sqlite")
            c = await o.cursor()
            await c.execute(f"SELECT * FROM bots WHERE bot = '{bot.id}'")
            rows1 = await c.fetchall()
            await c.execute(f"SELECT * FROM bots WHERE owner = '{owner.id}'")
            rows2 = await c.fetchall()
            if not rows1 and not rows2:
                await c.execute(f"INSERT INTO bots(bot, owner) VALUES('{bot.id}', '{owner.id}')")
                await o.commit()
                await o.close()
                await ctx.send(f"<:cs_id:659355469034422282> {ctx.author.mention} - 이제 봇 `{bot}`은 `{owner}`에게 귀속됩니다.")
                bown = ctx.guild.get_role(806785430044803132)
                await owner.add_roles(bown)
            else:
                raise commands.BadArgument
        else:
            raise commands.BadArgument
    
    @commands.command(name="해제")
    @commands.has_role(711753639722745896)
    async def _unregister(self, ctx, member: discord.Member):
        o = await aiosqlite.connect("Shark1ight.sqlite")
        c = await o.cursor()
        await c.execute(f"SELECT * FROM bots WHERE bot = '{member.id}' OR owner = '{member.id}'")
        rows = await c.fetchall()
        if not rows:
            raise commands.UserNotFound
        else:
            await c.execute(f"DELETE FROM bots WHERE bot = '{member.id}' OR owner = '{member.id}'")
            await o.commit()
            await o.close()
            bot = self.bot.get_user(int(rows[0][0]))
            owner = self.bot.get_user(int(rows[0][1]))
            await ctx.send(f"<:cs_id:659355469034422282> {ctx.author.mention} - 이제 봇 `{bot}`는 더 이상 `{owner}`에게 귀속되지 않습니다.")
            bown = ctx.guild.get_role(806785430044803132)
            await owner.remove_roles(bown)

def setup(bot):
    bot.add_cog(Developers(bot))