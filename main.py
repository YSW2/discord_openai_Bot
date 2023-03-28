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

	content = message.content
	prompts = []
	tasks = []
	name = []
	if content.startswith(prefix):
		prompts.append([message.author, content[1:]])
		for nick, prompt in prompts:
			name.append(nick)
			tasks.append(asyncio.ensure_future(openai_bot.usegpt(prompt)))
		responses = await asyncio.gather(*tasks)

		for i, response in enumerate(responses):
			index = 0
			while index < len(response):
				await message.channel.send(f"{name[i].mention}{response[index: min(index+2000, len(response))]}")
				index += 2000
	tasks.clear()
	name.clear()

bot.run(token)