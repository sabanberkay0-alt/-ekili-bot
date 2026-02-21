import os
import discord
import random
import asyncio
from discord.ext import commands

# TOKEN Railway Variables'dan gelecek
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN bulunamadı! Railway Variables kontrol et.")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} aktif!")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def cekilis(ctx, sure: int, kazanan_sayisi: int, *, odul: str):

    embed = discord.Embed(
        title="🎉 ÇEKİLİŞ BAŞLADI 🎉",
        description=(
            f"🎁 Ödül: **{odul}**\n"
            f"⏳ Süre: **{sure} saniye**\n"
            f"🏆 Kazanan Sayısı: **{kazanan_sayisi}**\n\n"
            "Katılmak için 🎉 reaksiyonuna bas!"
        ),
        color=discord.Color.gold()
    )

    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🎉")

    await asyncio.sleep(sure)

    msg = await ctx.channel.fetch_message(msg.id)
    reaction = discord.utils.get(msg.reactions, emoji="🎉")

    if not reaction:
        await ctx.send("❌ Kimse katılmadı.")
        return

    users = [user async for user in reaction.users() if not user.bot]

    if not users:
        await ctx.send("❌ Kimse katılmadı.")
        return

    kazananlar = random.sample(users, min(kazanan_sayisi, len(users)))
    kazanan_text = ", ".join(user.mention for user in kazananlar)

    await ctx.send(f"🎉 Kazanan(lar): {kazanan_text}\n🏆 Ödül: **{odul}**")

bot.run(TOKEN)
