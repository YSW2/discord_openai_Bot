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


@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name =f"{bot.command_prefix}"))

@bot.event
async def on_message(message):
	if message.author.bot:
		return
	
	content = message.content
	prompts = []
	'''if content.startswith(prefix):
		result = await chatgpt.usegpt(content[1:])
		await message.channel.send(result)'''
	if content.startswith(prefix):
		tasks = []
		name = []
		nickname = message.author.nick if message.author.nick else message.author.name
		prompts.append([nickname, content])
		for nick, prompt in prompts:
			name.append(nick)
			tasks.append(asyncio.ensure_future(openai_api.usegpt(prompt)))
		responses = await asyncio.gather(*tasks)

		for i in range(len(responses)):
			await message.channel.send(f"{name[i]}/ {responses[i]}")
	
bot.run(token)