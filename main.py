from pathlib import Path
import telebot
import os
from src.TelegramBot.TelegramBotController import TelegramBotController
from dotenv import load_dotenv
from src.DeepFace.DeepFaceController import DeepFaceController

# Включить .env
load_dotenv()

# Инициализация DeepFace
deep_face_controller = DeepFaceController()

# Инициализация бота
bot_telegram = telebot.TeleBot(os.getenv("TELEGRAM_BOT_KEY"))
telegram_bot_controller = TelegramBotController(
    bot=bot_telegram,
    deep_face_controller=deep_face_controller)
telegram_bot_controller.start()