import discord
from discord.ext import commands
import aiosqlite
import datetime

class Ticket(commands.Cog, name="티켓 지원 시스템"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.emoji) == "<:cs_leave:659355468803866624>":
            g = self.bot.get_guild(payload.guild_id)
            ch = g.get_channel(payload.channel_id)
            if ch.name.startswith("티켓_"):
                member = g.get_member(int(ch.topic))
                await ch.set_permissions(member, overwrite=None)
                name = ch.name.replace("티켓", "종료")
                await ch.edit(name=name)
                try:
                    await member.send(f"<:cs_leave:659355468803866624> {member.mention} - 당신이 열었던 티켓이 닫혔어요. 다시 여시려면 `상어 티켓 [ 채널 ID ]`를 사용해주세요.\n채널 ID : {ch.id}")
                except:
                    print("Discord 개인 메시지가 차단되어 전송하지 않았습니다.")
    
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
            embed.set_thumbnail(url=msg.author.avatar_url_as(static_format="png", size=2048))
            embed.set_footer(text="티켓을 통한 지원 시스템", icon_url=self.bot.user.avatar_url)
            msg = await channel.send("@here", embed=embed)
            await msg.add_reaction("<:cs_leave:659355468803866624>")
            await msg.pin()
            await c.execute(f'UPDATE shark SET ticket = {int(rows[0][1]) + 1}')
            await o.commit()
            await o.close()
    
    @commands.command(name="티켓")
    async def _reopen(self, ctx, channel: discord.TextChannel):
        if channel.name.startswith("종료_"):
            if ctx.author.id == channel.topic or ctx.author.top_role.id == 711753639722745896:
                member = ctx.guild.get_member(int(channel.topic))
                name = channel.name.replace("종료", "티켓")
                await channel.edit(name=name)
                overwrite = discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True, manage_roles=True)
                await channel.set_permissions(member, overwrite=overwrite)
                message = None
                async for msg in channel.history(limit=200):
                    if msg.author == self.bot.user:
                        message = msg
                await message.reply("<:cs_yes:659355468715786262> @here - 지원 티켓이 소유자 혹은 관리자에 의해 다시 열렸어요!")
                await ctx.message.add_reaction("<:cs_yes:659355468715786262>")

def setup(bot):
    bot.add_cog(Ticket(bot))