from pathlib import Path
import telebot
import os
from src.TelegramBot.TelegramBotController import TelegramBotController
from dotenv import load_dotenv
from src.DeepFace.DeepFaceController import DeepFaceController
from src.Pytesseract.PytesseractController import PytesseractController
from src.YOLOController.YOLOController import YOLOController

# Включить .env
load_dotenv()

# Инициализация DeepFace
deep_face_controller = DeepFaceController()
yolo_controller = YOLOController()

# Инициализация Pytesseract
pytesseract_contoller = PytesseractController(os.getenv("TESSERACT_BIN"))

# Инициализация бота
bot_telegram = telebot.TeleBot(os.getenv("TELEGRAM_BOT_KEY"))
telegram_bot_controller = TelegramBotController(
    bot=bot_telegram,
    deep_face_controller=deep_face_controller,
    pytesseract_contoller=pytesseract_contoller,
    yolo_controller=yolo_controller
    )
telegram_bot_controller.start()