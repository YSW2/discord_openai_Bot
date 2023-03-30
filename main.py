import discord
import asyncio
from discord.ext import commands
import openai_api
import json
import os

token = os.getenv("discord_API_KEY")

# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	prefix = data["prefix"]
	owner_id = data["owner_id"]


# Intents
intents = discord.Intents.all()
# The bot
bot = commands.Bot(command_prefix=prefix, intents=intents)
openai_bot = openai_api.openai_bot()

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name =f"{bot.command_prefix}"))

@bot.command()
async def clear(ctx):
	await openai_bot.messages_clear()
	await ctx.send("청소 완료")
	
@bot.event
async def on_message(message):
	if message.author.bot or message.content[1:] == "clear":
		await bot.process_commands(message)
		return

	if message.content.startswith(prefix):
		prompt = message.content[1:]
		response = await openai_bot.usegpt(prompt)
		for index in range(0, len(response), 2000):
			await message.channel.send(f"{message.author.mention}{response[index: index+2000]}")
			
bot.run(token)