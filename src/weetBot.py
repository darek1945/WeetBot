import discord
import time
from discord.ext import commands
import os
from scraper import fetch_availability  # Import from scraper.py

urls = {
    "Cannabis Flos THC 18% CBD ≤ 1% (S-Lab)": "https://www.gdziepolek.pl/produkty/117668/cannabis-flos-thc-18-cbd-1-s-lab-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 22% CBD ≤1% (S-Lab)": "https://www.gdziepolek.pl/produkty/121591/cannabis-flos-thc-22-cbd-1-s-lab-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    # ... pozostale URL (ostatnie paramsy definiuja miasto w-katowicach = apteki w katowicach)
}

CACHE_TIMEOUT = 600
cache = {}

CHECK_COMMAND = "s"
CHECK_ALIASES = ['sprawdz', 'check']
LIST_COMMAND = "l"
LIST_ALIASES = ['lista', 'list']

def get_cached_data(url):
    data, timestamp = cache.get(url, (None, 0))
    if time.time() - timestamp < CACHE_TIMEOUT:
        return data
    return None

def set_cache_data(url, data):
    cache[url] = (data, time.time())

def format_message(data_by_drug):
    message_parts = []
    for drug, entries in data_by_drug.items():
        message = f"🌻  {drug}  🌻 \n\n{'⬇️🔽⏬⏬🔽⬇️'*2}\n\n"
        for entry in entries:
            status_icon = get_status_icon(entry[2])
            part = (
                f"⚕️  {entry[0]}\n"
                f"🗺️  {entry[1]}\n"
                f"⛽  {status_icon} {entry[2]} {status_icon}\n"
                f"🎍  {entry[3]}\n"
                f"📉  {entry[5]}\n\n"
            )
            message += part
        if len(message) > 2000:
            message_parts.append(message)
            message = ""
        else:
            message_parts.append(message)
    return message_parts

def get_status_icon(status):
    if "wiele sztuk" in status:
        return "🟢"
    elif "kilka sztuk" in status:
        return "🟡"
    elif "niepełne opakowanie" in status:
        return "🟠"
    elif "ostatnia sztuka" in status:
        return "🔴"
    return "🔴"

async def check_availability(ctx, indices):
    selected_urls = {name: url for idx, (name, url) in enumerate(urls.items()) if idx + 1 in indices}
    if not selected_urls:
        await ctx.send("Nie znaleziono leków o podanych indeksach.")
        return

    data_by_drug = {}
    for name, url in selected_urls.items():
        data = get_cached_data(url) or fetch_availability(url)
        set_cache_data(url, data)
        data_by_drug[name] = data

    if not data_by_drug:
        await ctx.send("Brak dostępnych leków w wybranych aptekach.")
        return
    
    message_parts = format_message(data_by_drug)
    for part in message_parts:
        if part:
            await ctx.send(part)

intents = discord.Intents.default()
intents.message_content = True
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.command(name=CHECK_COMMAND, aliases=CHECK_ALIASES)
async def check_command(ctx, *args):
    indices = [int(i) for i in args if i.isdigit()]
    await check_availability(ctx, indices)

@bot.command(name=LIST_COMMAND, aliases=LIST_ALIASES)
async def list_drugs(ctx):
    message = "Lista leków:\n\n" + "\n".join([f"{idx}. {name}" for idx, name in enumerate(urls.keys(), 1)])
    await ctx.send(message)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()
    if content.startswith(tuple([CHECK_COMMAND] + CHECK_ALIASES)):
        indices = [int(i) for i in content.split()[1:] if i.isdigit()]
        await check_availability(message.channel, indices)
    elif content.startswith(tuple([LIST_COMMAND] + LIST_ALIASES)):
        await list_drugs(message.channel)

    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}')

bot.run(TOKEN)