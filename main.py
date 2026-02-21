import os
import discord
import random
import asyncio
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} aktif!")

@bot.command()
async def cekilis(ctx, sure: int, kazanan_sayisi: int, *, odul: str):
    embed = discord.Embed(
        title="🎉 ÇEKİLİŞ 🎉",
        description=f"Ödül: **{odul}**\nSüre: **{sure} saniye**\nKazanan: **{kazanan_sayisi}**\n\nKatılmak için 🎉 bas!",
        color=discord.Color.gold()
    )

    mesaj = await ctx.send(embed=embed)
    await mesaj.add_reaction("🎉")

    await asyncio.sleep(sure)

    mesaj = await ctx.channel.fetch_message(mesaj.id)
    reaction = discord.utils.get(mesaj.reactions, emoji="🎉")

    if not reaction:
        await ctx.send("❌ Katılım yok.")
        return

    users = [user async for user in reaction.users() if not user.bot]

    if not users:
        await ctx.send("❌ Katılım yok.")
        return

    kazananlar = random.sample(users, min(kazanan_sayisi, len(users)))

    kazanan_text = ", ".join(u.mention for u in kazananlar)

    await ctx.send(f"🎉 Kazanan(lar): {kazanan_text} 🎉")

bot.run(TOKEN)
