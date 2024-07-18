import logging
import time
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from common import fetch_data, get_cached_data, set_cache_data  # Importujemy z common.py
import config 
from helpers import format_message
import strings  # Importujemy strings.py

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_availability(update: Update, context: ContextTypes.DEFAULT_TYPE):
    indices = [int(i) for i in context.args if i.isdigit()]
    selected_urls = {name: url for idx, (name, url) in enumerate(config.urls.items()) if idx + 1 in indices}
    if not selected_urls:
        await update.message.reply_text(strings.DRUGS_NOT_FOUND)
        return

    tasks = [fetch_data(name, url) for name, url in selected_urls.items()]
    results = await asyncio.gather(*tasks)
    data_by_drug = {name: data for name, data in results if data}

    if not data_by_drug:
        await update.message.reply_text(strings.NO_AVAILABLE_DRUGS)
        return
    
    message_parts = format_message(data_by_drug)
    for part in message_parts:
        if part:
            await update.message.reply_text(part)

async def list_drugs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = strings.DRUG_LIST_HEADER + "\n".join([f"{idx}. {name}" for idx, name in enumerate(config.urls.keys(), 1)])
    await update.message.reply_text(message)

def main():
    application = ApplicationBuilder().token(config.TOKEN).build()

    check_handler = CommandHandler(config.CHECK_COMMAND, check_availability)
    list_handler = CommandHandler(config.LIST_COMMAND, list_drugs)

    application.add_handler(check_handler)
    application.add_handler(list_handler)

    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
