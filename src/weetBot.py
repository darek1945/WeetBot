import discord
import time
from discord.ext import commands, tasks
import os
from scraper import fetch_availability  # Import from scraper.py

urls = {
    "Cannabis Flos THC 18% CBD ≤ 1% (S-Lab)": "https://www.gdziepolek.pl/produkty/117668/cannabis-flos-thc-18-cbd-1-s-lab-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 22% CBD ≤1% (S-Lab)": "https://www.gdziepolek.pl/produkty/121591/cannabis-flos-thc-22-cbd-1-s-lab-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Sativa L., Red No 2 (Canopy Growth)": "https://www.gdziepolek.pl/produkty/98013/cannabis-sativa-l-red-no-2-canopy-growth-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 20% CBD 1% (Aurora) Pink Kush": "https://www.gdziepolek.pl/produkty/119768/cannabis-flos-thc-20-cbd-1-aurora-pink-kush-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 18% CBD 1% (Tilray)": "https://www.gdziepolek.pl/produkty/117669/cannabis-flos-thc-18-cbd-1-tilray-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis flos THC 22%, CBD <1% (Four 20 Pharma GmbH) Gorilla Glue": "https://www.gdziepolek.pl/produkty/120136/cannabis-flos-thc-22-cbd-1-four-20-pharma-gmbh-gorilla-glue-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 22% CBD 1% (Aurora Deutschland GmbH) Ghost Train Haze": "https://www.gdziepolek.pl/produkty/100242/cannabis-flos-thc-22-cbd-1-aurora-deutschland-gmbh-ghost-train-haze-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 20 % CBD <1% (ODI Pharma) Bienville (Jean Guy)": "https://www.gdziepolek.pl/produkty/119465/cannabis-flos-thc-20-cbd-1-odi-pharma-bienville-jean-guy-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis flos THC 20%, CBD <1% (Four 20 Pharma GmbH) Gorilla Glue": "https://www.gdziepolek.pl/produkty/120135/cannabis-flos-thc-20-cbd-1-four-20-pharma-gmbh-gorilla-glue-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 22% CBD 1% (Aurora) Delahaze": "https://www.gdziepolek.pl/produkty/119767/cannabis-flos-thc-22-cbd-1-aurora-delahaze-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 20% CBD 1% (Medezin) Amnesia Haze": "https://www.gdziepolek.pl/produkty/121592/cannabis-flos-thc-20-cbd-1-medezin-amnesia-haze-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 8%, CBD 7% (Canopy Growth) Penelope": "https://www.gdziepolek.pl/produkty/110500/cannabis-flos-thc-8-cbd-7-canopy-growth-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 22% CBD ≤ 1% (S-Lab)": "https://www.gdziepolek.pl/produkty/121591/cannabis-flos-thc-22-cbd-1-s-lab-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 25%, CBD ≤ 0,5% (Canopy Growth) Krypton": "https://www.gdziepolek.pl/produkty/126179/cannabis-flos-thc-25-cbd-0-5-canopy-growth-krypton-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 8% CBD 8% (Aurora Deutschland GmbH) Equiposa": "https://www.gdziepolek.pl/produkty/100241/cannabis-flos-thc-8-cbd-8-aurora-deutschland-gmbh-equiposa-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 20%, CBD ≤ 0,5% (Canopy Growth)": "https://www.gdziepolek.pl/produkty/115281/cannabis-flos-thc-20-cbd-0-5-canopy-growth-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis flos THC 16% CBD <0,5% (Canopy Growth)": "https://www.gdziepolek.pl/produkty/126274/cannabis-flos-thc-16-cbd-0-5-canopy-growth-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 10%, CBD 7% (Canopy Growth)": "https://www.gdziepolek.pl/produkty/101446/cannabis-flos-thc-10-cbd-7-canopy-growth-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 20% CBD 1% (Aurora Deutschland GmbH) L.A Confidential": "https://www.gdziepolek.pl/produkty/100243/cannabis-flos-thc-20-cbd-1-aurora-deutschland-gmbh-l-a-confidential-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 1% CBD 12% (Aurora)": "https://www.gdziepolek.pl/produkty/100244/cannabis-flos-thc-1-cbd-12-aurora-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 20% CBD 0,1% (IMP&C)": "https://www.gdziepolek.pl/produkty/126215/cannabis-flos-thc-20-cbd-0-1-impc-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 18% CBD ≤1% (Polfarmex)": "https://www.gdziepolek.pl/produkty/118367/cannabis-flos-thc-18-cbd-1-polfarmex-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 17% CBD <1% (CanPoland) Shiskaberry": "https://www.gdziepolek.pl/produkty/119466/cannabis-flos-thc-17-cbd-1-canpoland-shiskaberry-marihuana-lecznicza-medyczna/apteki/w-gliwicach",
    "Cannabis Flos THC 22% CBD <1% (CanPoland) Gorilla Glue": "https://www.gdziepolek.pl/produkty/119467/cannabis-flos-thc-22-cbd-1-canpoland-gorilla-glue-marihuana-lecznicza-medyczna/apteki/w-gliwicach"
}

# Cache 10 min
CACHE_TIMEOUT = 600
cache = {}

def get_cached_data(url):
    if url in cache:
        data, timestamp = cache[url]
        if time.time() - timestamp < CACHE_TIMEOUT:
            return data
    return None

def set_cache_data(url, data):
    cache[url] = (data, time.time())


def format_message(data_by_drug):
    message_parts = []
    for drug, entries in data_by_drug.items():
        message = f"🌻  {drug}  🌻 \n{'_'}\n"
        for entry in entries:
            status_icon = "🔴"
            if "wiele sztuk" in entry[2]:
                status_icon = "🟢"
            elif "kilka sztuk" in entry[2]:
                status_icon = "🟡"
            elif "niepełne opakowanie" in entry[2]:
                status_icon = "🟠"
            elif "ostatnia sztuka" in entry[2]:
                status_icon = "🔴"
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

async def check_availability(ctx, indices):
    selected_urls = {name: url for idx, (name, url) in enumerate(urls.items()) if idx + 1 in indices}
    
    if not selected_urls:
        await ctx.send("Nie znaleziono leków o podanych indeksach.")
        return

    data_by_drug = {}
    for name, url in selected_urls.items():
        cached_data = get_cached_data(url)
        if cached_data is not None:
            data = cached_data
        else:
            data = fetch_availability(url)
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


@bot.command(name='sprawdz', aliases=['s'])
async def check_command(ctx, *args):
    indices = [int(i) for i in args if i.isdigit()]
    await check_availability(ctx, indices)


@bot.command(name='lista', aliases=['l'])
async def list_drugs(ctx):
    message = "Lista leków:\n\n"
    for idx, name in enumerate(urls.keys(), 1):
        message += f"{idx}. {name}\n"
    await ctx.send(message)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()

    if content.startswith('sprawdz') or content.startswith('s'):
        args = content.split()[1:]
        indices = [int(i) for i in args if i.isdigit()]
        await check_availability(message.channel, indices)

    elif content.startswith('lista') or content.startswith('l'):
        response = "Lista leków:\n\n"
        for idx, name in enumerate(urls.keys(), 1):
            response += f"{idx}. {name}\n"
        await message.channel.send(response)

    await bot.process_commands(message)


@bot.event
async def on_ready():
    print(f'Zalogowano jako {bot.user}')

bot.run(TOKEN)
