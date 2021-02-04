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
    async def on_message(self, msg):
        if msg.author.bot:
            return
        
        if msg.channel.id == 803190240714031104:
            await msg.delete()
            category = msg.guild.get_channel(806796478458626048)
            overwrites = {
                msg.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                msg.author: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True, manage_roles=True)
            }
            o = await aiosqlite.connect("Shark1ight.sqlite")
            c = await o.cursor()
            await c.execute("SELECT * FROM shark")
            rows = await c.fetchall()
            number = ""
            for i in range(len(str(rows[0][1])), 4):
                number += "0"
            number += str(rows[0][1])
            channel = await category.create_text_channel(name=f"티켓_{number}", overwrites=overwrites, topic=msg.author.id)
            embed = discord.Embed(title=f"{msg.author}님의 새 지원 요청입니다!", description=f"지원 요청 사유 : {msg.content}\n티켓을 닫으시려면 아래에 있는 반응을 눌러주세요.", color=0xAFFDEF, timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=msg.author.avatar_url_as(format="png", size=2048))
            embed.set_footer(text="티켓을 통한 지원 시스템", icon_url=self.bot.user.avatar_url)
            msg = await channel.send("@here", embed=embed)
            await msg.add_reaction("<:cs_leave:659355468803866624>")
            await msg.pin()
            await c.execute(f'UPDATE shark SET ticket = {int(rows[0][1]) + 1}')
            await o.commit()
            await o.close()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.bot:
            role = member.guild.get_role(806789561665323038)
            await member.add_roles(role)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        mute = member.guild.get_roles(803182061229703168)
        if mute in member.roles:
            await member.guild.ban(member, reason="뮤트 역할을 가진 채로 서버에서 퇴장.")

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
        else:
            if str(payload.emoji) == "<:cs_leave:659355468803866624>":
                g = self.bot.get_guild(payload.guild_id)
                ch = g.get_channel(payload.channel_id)
                if ch.name.startswith("티켓_"):
                    member = g.get_member(int(ch.topic))
                    await ch.set_permissions(member, overwrite=None)
                    name = ch.name.replace("티켓", "종료")
                    await ch.edit(name=name)
                    await member.send(f"<:cs_leave:659355468803866624> {member.mention} - 당신이 열었던 티켓이 닫혔어요. 다시 여시려면 `상어 티켓 [ 채널 ID ]`를 사용해주세요.\n채널 ID : {ch.id}")
    
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
        embed.set_thumbnail(url=self.bot.user.avatar_url_as(format="png", size=2048))
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
    