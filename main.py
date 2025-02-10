from pathlib import Path
import telebot
import os
from src.TelegramBot.TelegramBotController import TelegramBotController
from dotenv import load_dotenv
from src.DeepFace.DeepFaceController import DeepFaceController
from googletrans import Translator

# Включить .env
load_dotenv()

# Инициализация DeepFace
deep_face_controller = DeepFaceController()

# Инициализация переводчика
translator = Translator()

# Инициализация бота
bot_telegram = telebot.TeleBot(os.getenv("TELEGRAM_BOT_KEY"))
telegram_bot_controller = TelegramBotController(
    bot=bot_telegram,
    deep_face_controller=deep_face_controller,
    translator=translator,
    )
telegram_bot_controller.start()