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
    asyncio.run_coroutine_threadsafe(
        bot.change_presence(status=discord.Status.online, activity=discord.Game(name=status_text)),
        bot.loop
    )
    return {"message": "Status updated"}, 200

@app.route("/player/join", methods=["POST"])
def player_join():
    data = request.json
    player_count = data["PlayerCount"]
    max_players = data["MaxPlayers"]

    channel_id = 1419504760482037883
    channel = bot.get_channel(channel_id)
    if channel:
        asyncio.run_coroutine_threadsafe(
            channel.send(f"Player count: {player_count}\nMax players: {max_players}"),
            bot.loop
        )

    status_game = discord.Game(f"{player_count}/{max_players}")
    asyncio.run_coroutine_threadsafe(
        bot.change_presence(status=discord.Status.online, activity=status_game),
        bot.loop
    )

    return {"message": "Player join posted"}, 200

@app.route("/player/leave", methods=["POST"])
def player_leave():
    data = request.json
    nickname = data.get("Nickname")
    player_count = data.get("PlayerCount", 0)
    max_players = data.get("MaxPlayers", 0)

    channel_id = 1419504760482037883
    channel = bot.get_channel(channel_id)
    if channel:
        asyncio.run_coroutine_threadsafe(
            channel.send(f"Player left: {nickname} - Players: {player_count}/{max_players}"),
            bot.loop
        )

        status_game = discord.Game(f"{player_count}/{max_players}")
        asyncio.run_coroutine_threadsafe(
            bot.change_presence(status=discord.Status.online, activity=status_game),
            bot.loop
        )

    return {"message": "Player leave posted"}, 200

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot is ready as {bot.user}")

async def load_cmds():
    for file in os.listdir("./commands"):
        if file.endswith(".py"):
            await bot.load_extension(f"commands.{file[:-3]}")

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