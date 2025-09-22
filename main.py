import os
import discord
import asyncio
import threading

from flask import Flask, request
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

app = Flask(__name__)
bot = commands.Bot(command_prefix="$", intents=intents)

@app.route("/update_status", methods=["POST"])
def update_status():
    data = request.json
    status_text = data.get("status", "Idle")
    game = discord.Game(name=status_text)
    bot.loop.create_task(bot.change_presence(status=discord.Status.online, activity=game))

    return {"message": "Status updated"}, 200

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is ready as {bot.user}")

async def load_cmds():
    for file in os.listdir("./commands"):
        if file.endswith(".py"):
            await bot.load_extension(f"commands.{file[:-3]}") # :3

def run_flask():
    app.run(host="0.0.0.0", port=5000)

async def main():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    async with bot:
        await load_cmds()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())