import discord
import asyncio
import logging
from discord.ext import commands
from common import fetch_data, get_cached_data, set_cache_data  # Importujemy z common.py
import config 
from helpers import format_message
import strings  # Importujemy strings.py

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_availability(ctx, indices):
    selected_urls = {name: url for idx, (name, url) in enumerate(config.urls.items()) if idx + 1 in indices}
    if not selected_urls:
        await ctx.send(strings.DRUGS_NOT_FOUND)
        return

    tasks = [fetch_data(name, url) for name, url in selected_urls.items()]
    results = await asyncio.gather(*tasks)
    data_by_drug = {name: data for name, data in results if data}

    if not data_by_drug:
        await ctx.send(strings.NO_AVAILABLE_DRUGS)
        return
    
    message_parts = format_message(data_by_drug)
    for part in message_parts:
        if part:
            await ctx.send(part)

def create_bot():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='/', intents=intents)
    return bot

bot = create_bot()

@bot.command(name=config.CHECK_COMMAND, aliases=config.CHECK_ALIASES)
async def check_command(ctx, *args):
    indices = [int(i) for i in args if i.isdigit()]
    await check_availability(ctx, indices)

@bot.command(name=config.LIST_COMMAND, aliases=config.LIST_ALIASES)
async def list_drugs(ctx):
    message = strings.DRUG_LIST_HEADER + "\n".join([f"{idx}. {name}" for idx, name in enumerate(config.urls.keys(), 1)])
    await ctx.send(message)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()
    if content.startswith(tuple([config.CHECK_COMMAND] + config.CHECK_ALIASES)):
        indices = [int(i) for i in content.split()[1:] if i.isdigit()]
        await check_availability(message.channel, indices)
    elif content.startswith(tuple([config.LIST_COMMAND] + config.LIST_ALIASES)):
        await list_drugs(message.channel)

    await bot.process_commands(message)

@bot.event
async def on_ready():
    logger.info(f'Zalogowano jako {bot.user}')

bot.run(config.TOKEN)
