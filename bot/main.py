import os
from discord.ext import commands
from utils.CustomBot import CustomBot

bot = CustomBot(command_prefix="!")
bot.embed_color = 0x2F3136
TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

if __name__ == "__main__":
    bot.run(TOKEN)
