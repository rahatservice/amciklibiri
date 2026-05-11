import os
import discord
from discord.ext import commands
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)

# =========================
# DATA
# =========================

kayit_sayisi = 0

ROLE_IDS = {
    "Teknik Direktör┇💼": 1503341802646802434,
    "Üye┇👤": 1503341807310999592,
    "Bayan Üye┇🎀": 1503341778915299338,
    "Başkan┇🤵🏻‍♂️": 1503341801568866315,
    "Futbolcu┇🧩": 1503341805293277285
}

KAYITSIZ_ROLE_ID = 1503341810368381058
YETKILI_ROLE_ID = 1503341765178953739


# =========================
# REGISTER MENU
# =========================

class RegisterView(discord.ui.View):
    def __init__(self, member: discord.Member):
        super().__init__(timeout=60)
        self.member = member

        options = [
            discord.SelectOption(label=name, value=name)
            for name in ROLE_IDS.keys()
        ]

        self.add_item(RoleSelect(options, member))


class RoleSelect(discord.ui.Select):
    def __init__(self, options, member):
        super().__init__(
            placeholder="Rol seç… hayatını seçiyorsun 😏",
            options=options
        )
        self.member = member

    async def callback(self, interaction: discord.Interaction):
        global kayit_sayisi

        guild = interaction.guild
        role_name = self.values[0]

        role = guild.get_role(ROLE_IDS[role_name])
        kayitsiz = guild.get_role(KAYITSIZ_ROLE_ID)

        await self.member.add_roles(role)

        if kayitsiz:
            await self.member.remove_roles(kayitsiz)

        kayit_sayisi += 1

        await interaction.response.edit_message(
            content=f"✔️ {self.member.mention} kayıt edildi → **{role_name}**",
            view=None
        )


# =========================
# COMMANDS
# =========================

@bot.command()
async def k(ctx, member: discord.Member, *, isim: str):

    if YETKILI_ROLE_ID not in [r.id for r in ctx.author.roles]:
        return await ctx.send("❌ Bu komutu sadece Kayıt Yetkilisi kullanabilir.")

    await ctx.send(f"📋 Kayıt başlatıldı: **{member}** → isim: **{isim}**")

    view = RegisterView(member)
    await ctx.send("Rol seç:", view=view)


@bot.command()
async def kayitsayi(ctx):
    await ctx.send(f"📊 Toplam kayıt sayısı: **{kayit_sayisi}**")


# =========================
# JOIN EVENT
# =========================

@bot.event
async def on_member_join(member):

    channel = discord.utils.get(member.guild.text_channels, name="general")
    role_mention = f"<@&{YETKILI_ROLE_ID}>"

    embed = discord.Embed(
        title=f"{member.name} sunucuya geldi",
        description=f"Hoş geldin {member.mention}\nYetkililer: {role_mention}",
        color=discord.Color.green()
    )

    if channel:
        await channel.send(embed=embed)


# =========================
# READY EVENT
# =========================

@bot.event
async def on_ready():
    print(f"Bot aktif: {bot.user}")


bot.run(TOKEN)
