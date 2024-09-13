from pathlib import Path
import telebot
import os
import uuid
from src.TelegramBot.TelegramBotController import TelegramBotController
from dotenv import load_dotenv

# Включить .env
load_dotenv()

# Инициализация бота
bot = telebot.TeleBot(os.getenv("TELEGRAM_BOT_KEY"))
bot_telegram = TelegramBotController(bot)
bot_telegram.start()