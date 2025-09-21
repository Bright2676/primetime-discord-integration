import os
import discord
import asyncio
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is ready as {bot.user}")

async def load_cmds():
    for file in os.listdir("./commands"):
        if file.endswith(".py"):
            await bot.load_extension(f"commands.{file[:-3]}") # :3

async def main():
    async with bot:
        await load_cmds()
        await bot.start(TOKEN)

asyncio.run(main())