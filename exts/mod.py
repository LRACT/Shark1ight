import discord
from discord.ext import commands
import typing
import aiosqlite
from pytz import timezone, utc
import datetime
import asyncio

def kor_time(date):
    KST = timezone('Asia/Seoul')
    abc = utc.localize(date).astimezone(KST)
    time = abc.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    return time

class Mod(commands.Cog, name="관리"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="경고")
    @commands.has_role(711753639722745896)
    async def _warn(self, ctx, task, member: discord.Member, *, reason: typing.Optional[str] = "사유가 지정되지 않음."):
        await ctx.message.delete()
        o = await aiosqlite.connect("Shark1ight.sqlite")
        c = await o.cursor()
        time = kor_time(datetime.datetime.utcnow())
        if task == "추가":
            await c.execute(f"SELECT * FROM warns WHERE user = '{member.id}'")
            rows = await c.fetchall()
            await c.execute(f"INSERT INTO warns(user, admin, reason, time) VALUES('{member.id}', '{ctx.author.id}', '{reason}', '{time}')")
            await o.commit()
            await o.close() 
            embed = discord.Embed(
                title=f"{member}님에게 경고 1회가 지급되었어요.",
                description=f"사유 : {reason}\n지급 일시 : {time}",
                timestamp=datetime.datetime.utcnow(),
                color=0xFFFCC9
            )
            embed.set_thumbnail(url=member.avatar_url_as(static_format="png", size=2048))
            embed.set_footer(text=f"실행자 : {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        elif task == "목록":
            await c.execute(f"SELECT * FROM warns WHERE user = '{member.id}'")
            rows = await c.fetchall()
            if not rows:
                await ctx.send(f"<:cs_no:659355468816187405> {ctx.author.mention} - 해당 유저에게는 경고 이력이 없어요.")
            else:
                a = ""
                i = 1
                for row in rows:
                    a += f"#{i} : {row[2]} - By {row[1]}\n    {row[3]}"
                    i += 1
                embed = discord.Embed(
                    title=f"{member}님의 현재 경고 목록이에요.",
                    description=a,
                    timestamp=datetime.datetime.utcnow(),
                    color=0xFFFCC9
                )
                embed.set_thumbnail(url=member.avatar_url_as(static_format="png", size=2048))
                embed.set_footer(text=f"실행자 : {ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed)
    
    @commands.command(name="뮤트")
    @commands.has_role(711753639722745896)
    async def _mute(self, ctx, member: discord.Member, *, reason: typing.Optional[str] = "사유가 지정되지 않음."):
        await ctx.message.delete()
        mute = ctx.guild.get_role(803182061229703168)
        time = kor_time(datetime.datetime.utcnow())
        if mute not in member.roles:
            await member.add_roles(mute)
            embed = discord.Embed(
                title=f"{member}님의 채팅이 차단되었어요.",
                description=f"사유 : {reason}\n뮤트 일시 : {time}",
                timestamp=datetime.datetime.utcnow(),
                color=0x2A2C2D
            )
            embed.set_thumbnail(url=member.avatar_url_as(static_format="png", size=2048))
            embed.set_footer(text=f"실행자 : {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            await member.remove_roles(mute)
            embed = discord.Embed(
                title=f"{member}님의 채팅 차단이 해제되었어요.",
                description=f"사유 : {reason}\n언뮤트 일시 : {time}",
                timestamp=datetime.datetime.utcnow(),
                color=0x7E7E7E
            )
            embed.set_thumbnail(url=member.avatar_url_as(static_format="png", size=2048))
            embed.set_footer(text=f"실행자 : {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
    
    @commands.command(name="청소", aliases=["삭제"])
    @commands.has_role(711753639722745896)
    async def _purge(self, ctx, purge: int):
        if purge < 1 or purge > 100:
            raise commands.BadArgument
        else:
            await ctx.message.delete()
            deleted = await ctx.channel.purge(limit=purge)
            await ctx.send(f"<:cs_trash:659355468631769101> {ctx.author.mention} - **{len(deleted)}**개의 메시지가 삭제되었어요!", delete_after=3)

    @commands.command(name="슬로우", aliases=["슬로우모드"])
    @commands.has_role(711753639722745896)
    async def _slowmode(self, ctx, number: int):
        await ctx.message.delete()
        if number == 0:
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.send(f":stopwatch: {ctx.author.mention} - 채널의 슬로우 모드를 해제했어요.")
        elif number > 21600 or number <= 0:
            raise commands.BadArgument
        else:
            await ctx.channel.edit(slowmode_delay=number)
            await ctx.send(f":hourglass: {ctx.author.mention} - 채널을 *느 리 게  만 들 었 어 요 .*\n \n이제 모든 유저는 {number}초에 한 번만 메시지를 전송할 수 있어요.")

    @commands.command(name="추방", aliases=["킥"])
    @commands.has_role(711753639722745896)
    async def _kick(self, ctx, member: discord.Member, *, reason: typing.Optional[str] = "사유가 지정되지 않음."):
        await ctx.message.delete()
        time = kor_time(datetime.datetime.utcnow())
        if member.top_role < ctx.guild.me.top_role and member != ctx.guild.owner:
            try:
                await member.send(f"<a:ban_guy:761149578216603668> {ctx.author.mention} - 죄송하지만, **{ctx.guild.name}**에서 추방되셨습니다!\n사유 : {reason}\n처리한 관리자 : {ctx.author}")
            except:
                print("Discord 개인 메시지가 차단되어 전송하지 않았습니다.")
            await ctx.guild.kick(member, reason=reason)
            embed = discord.Embed(
                title=f"{member}님을 서버에서 추방했어요.",
                description=f"사유 : {reason}\n추방 일시 : {time}",
                timestamp=datetime.datetime.utcnow(),
                color=0xFF9999
            )
            embed.set_thumbnail(url=member.avatar_url_as(static_format="png", size=2048))
            embed.set_footer(text=f"실행자 : {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            raise commands.BadArgument
        
    @commands.command(name="차단", aliases=["밴", "벤"])
    @commands.has_role(711753639722745896)
    async def _ban(self, ctx, user: discord.Member, delete: typing.Optional[int] = 0, *, reason: typing.Optional[str] = "사유가 지정되지 않음."):
        await ctx.message.delete()
        time = kor_time(datetime.datetime.utcnow())
        if user.top_role < ctx.guild.me.top_role and user != ctx.guild.owner:
            try:
                await user.send(f"<a:ban_guy:761149578216603668> {ctx.author.mention} - 죄송하지만, **{ctx.guild.name}**에서 차단되셨습니다! 다시 접속하실 수 없음을 알립니다.\n사유 : {reason}\n처리한 관리자 : {ctx.author}")
            except:
                print("Discord 개인 메시지가 차단되어 전송하지 않았습니다.")
            await ctx.guild.ban(user, delete_message_days=delete, reason=reason)
            embed = discord.Embed(
                title=f"{user}님을 서버에서 차단했어요.",
                description=f"사유 : {reason}\n메시지 삭제 일수 : {delete}\n차단 일시 : {time}",
                timestamp=datetime.datetime.utcnow(),
                color=0xFF5555
            )
            embed.set_thumbnail(url=user.avatar_url_as(static_format="png", size=2048))
            embed.set_footer(text=f"실행자 : {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            raise commands.BadArgument

def setup(bot):
    bot.add_cog(Mod(bot))
