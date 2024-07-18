#!/bin/sh

if [ "$BOT" = "discord" ]; then
    echo "Starting discord bot"
    exec python discord_bot.py
elif [ "$BOT" = "telegram" ]; then
    echo "Starting telegram bot"
    exec python telegram_bot.py
else
    echo "Error: BOT environment variable not set correctly."
    exit 1
fi