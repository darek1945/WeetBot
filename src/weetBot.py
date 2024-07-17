import discord
import time
import asyncio
import logging
from discord.ext import commands
import aiohttp
from scraper import fetch_availability  # Import from scraper.py
import config 
from helpers import format_message, get_status_icon

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cache = {}

def get_cached_data(url):
    data, timestamp = cache.get(url, (None, 0))
    if time.time() - timestamp < config.CACHE_TIMEOUT:
        return data
    return None

def set_cache_data(url, data):
    cache[url] = (data, time.time())

async def fetch_data(name, url):
    cached_data = get_cached_data(url)
    if cached_data is not None:
        return name, cached_data
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html_content = await response.text()
        data = fetch_availability(html_content)
        set_cache_data(url, data)
        logger.info(f"Fetched data for {url}") 
        return name, data
    except Exception as e:
        logger.error(f"Error fetching data for {url}: {e}")
        return name, []

async def check_availability(ctx, indices):
    selected_urls = {name: url for idx, (name, url) in enumerate(config.urls.items()) if idx + 1 in indices}
    if not selected_urls:
        await ctx.send("Nie znaleziono leków o podanych indeksach.")
        return

    tasks = [fetch_data(name, url) for name, url in selected_urls.items()]
    results = await asyncio.gather(*tasks)
    data_by_drug = {name: data for name, data in results if data}

    if not data_by_drug:
        await ctx.send("Brak dostępnych leków w wybranych aptekach.")
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
    message = "Lista leków:\n\n" + "\n".join([f"{idx}. {name}" for idx, name in enumerate(config.urls.keys(), 1)])
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
