import discord
from discord.ext import commands
import datetime
import aiosqlite

class Listeners(commands.Cog, name="이벤트 리스너"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} - {self.bot.user.id} : 준비됨.")
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game("'상어 도움'에 답장"))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 702880464893116518:
            if member.bot:
                role = member.guild.get_role(806789561665323038)
                await member.add_roles(role)
            else:
                try:
                    embed = discord.Embed(
                        title=f"안녕하세요, {member}님! {member.guild.name}에 오신 것을 환영해요!",
                        description=f"이 서버는 개발자 분들이 편하게 소통할 수 있도록 제작된 서버에요.",
                        color=0xAFFDEF,
                        timestamp=datetime.datetime.utcnow()
                    )
                    embed.add_field(
                        name="개인 봇을 초대해 테스트하고 싶으신가요?",
                        value="봇 초대는 **Developer** 역할을 가진 분만 초대하실 수 있어요. <#803190103957831701> 채널을 확인해보세요!",
                        inline=False
                    )
                    await member.send(f"<:cs_notify:659355468904529920> {member.mention} - 반가워요!", embed=embed)
                except:
                    print("Discord 개인 메시지가 차단되어 전송하지 않았습니다.")
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 702880464893116518:
            mute = member.guild.get_roles(803182061229703168)
            if mute in member.roles:
                await member.guild.ban(member, reason="뮤트 역할을 가진 채로 서버에서 퇴장.")
            
            if member.bot:
                o = await aiosqlite.connect("Shark1ight.sqlite")
                c = await o.cursor()
                await c.execute(f"SELECT * FROM bots WHERE bot = '{member.id}'")
                rows = await c.fetchall()
                if rows:
                    owns = member.guild.get_member(int(rows[0][1]))
                    if owns is not None:
                        try:
                            await owns.send(f"<:cs_leave:659355468803866624> {owns.mention} - 당신의 봇 **{member}**이(가) **{member.guild.name}** 서버에서 퇴장되었습니다.")
                        except:
                            print("Discord 개인 메시지가 차단되어 전송하지 않았습니다.")
                    bown = member.guild.get_role(806785430044803132)
                    await owns.remove_roles(bown)
                    await c.execute(f"DELETE FROM bots WHERE bot = '{member.id}'")
                    await o.commit()
                    await o.close()
            else:
                o = await aiosqlite.connect("Shark1ight.sqlite")
                c = await o.cursor()
                await c.execute(f"SELECT * FROM bots WHERE owner = '{member.id}'")
                rows = await c.fetchall()
                if rows:
                    userbot = member.guild.get_member(int(rows[0][0]))
                    if userbot is not None:
                        await member.guild.kick(userbot, "봇 소유자가 서버에서 나감.")
                    await c.execute(f"DELETE FROM bots WHERE owner = '{member.id}'")
                    await o.commit()
                    await o.close()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return

        if payload.message_id == 806794580166180884:
            guild = self.bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            if str(payload.emoji) == "<:vscode:750666101842772058>":
                if guild is not None and user is not None:
                    role = guild.get_role(803186393304137738)
                    await user.add_roles(role, reason="본인 요청")
                    try:
                        await user.send(f"<:cs_yes:659355468715786262> {user.mention} - **{role.name}** 역할이 성공적으로 추가되었습니다!")
                    except:
                        print("Discord 개인 메시지가 차단되어 전송하지 않았습니다.")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 806794580166180884:
            guild = self.bot.get_guild(payload.guild_id)
            user = guild.get_member(payload.user_id)
            if str(payload.emoji) == "<:vscode:750666101842772058>":
                if guild is not None and user is not None:
                    role = guild.get_role(803186393304137738)
                    await user.remove_roles(role, reason="본인 요청")
                    try:
                        await user.send(f"<:cs_yes:659355468715786262> {user.mention} - **{role.name}** 역할이 성공적으로 삭제되었습니다!")
                    except:
                        print("Discord 개인 메시지가 차단되어 전송하지 않았습니다.")
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = discord.Embed(title="⚠️ 명령어 실행 도중 문제가 발생했어요!", timestamp=datetime.datetime.utcnow(), color=0xFF5555)
        embed.set_thumbnail(url=self.bot.user.avatar_url_as(static_format="png", size=2048))
        embed.set_footer(text=f"실행자 : {ctx.author}", icon_url=ctx.author.avatar_url)
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            if isinstance(error, commands.NotOwner):
                embed.description = "실행하신 명령어는 봇 관리자에 한해 사용이 제한됩니다."
            elif isinstance(error, commands.MissingRole) or isinstance(error, commands.MissingAnyRole):
                embed.description = "실행하신 명령어는 특정 역할을 가진 사용자에 한해 사용이 제한됩니다."
            elif isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
                if isinstance(error, commands.UserNotFound) or isinstance(error, commands.MemberNotFound):
                    embed.description = "파라미터로 필요한 유저가 발견되지 않았습니다."
                elif isinstance(error, commands.RoleNotFound):
                    embed.description = "파라미터로 필요한 역할이 발견되지 않았습니다."
                elif isinstance(error, commands.ChannelNotFound):
                    embed.description = "파라미터로 필요한 채널이 발견되지 않았습니다."
                elif isinstance(error, commands.ChannelNotReadable):
                    embed.description = "파라미터로 필요한 채널을 발견했으나, 봇이 읽을 수 없습니다."
                else:
                    embed.description = "파라미터로 제공된 값이 잘못되었거나, 없습니다."
            elif isinstance(error, commands.CheckAnyFailure) or isinstance(error, commands.CheckFailure):
                embed.description = "권한 및 유저 등의 환경 확인 작업에 실패했습니다."
            else:
                embed.description = f"예기치 않은 오류가 발생했습니다.\n``{error}``"
            embed.description += "\n자세한 내용은 관리자에게 문의해주십시오."
            await ctx.send(ctx.author.mention, embed=embed)
            

def setup(bot):
    bot.add_cog(Listeners(bot))
    