import uuid
from pathlib import Path
from telebot import types
from addict import Dict
from state.state import user_state
from state.dicts import genders
from colorthief import ColorThief
import math

# Контроллер для управления ботом
class TelegramBotController:
    def __init__(self, bot, deep_face_controller, translator):
        self.bot = bot
        self.deep_face_controller = deep_face_controller
        self.translator = translator
        self.register_handlers()


    # Регистрация всего на свете
    def register_handlers(self):
        self.bot.message_handler(commands=["start"])(self.start_command)
        self.bot.callback_query_handler(func=lambda call: True)(self.callback_query)
        self.bot.message_handler(content_types=["text"])(self.get_text_message)
        self.bot.message_handler(content_types=["photo"])(self.get_photo_messages)
        self.bot.message_handler(content_types=["document"])(self.get_document_messages)

    def start_command(self, message):
        keyboard = types.InlineKeyboardMarkup()
        button2 = types.InlineKeyboardButton("Получить анализ лица", callback_data="get_emotions")
        keyboard.add(button2)
        
        user_state[message.from_user.id] = Dict()
        user_state[message.from_user.id].keyboard_message = self.bot.send_message(
            message.chat.id,
            "Привет! Выбери то, чем хочешь заняться",
            reply_markup=keyboard
        )


    def callback_query(self, call):
        user = user_state[call.from_user.id]

        self.bot.delete_message(
            call.from_user.id,
            user.keyboard_message.message_id
        )

        user.call_data = call.data
        if call.data == "get_emotions":
            self.bot.send_message(
                call.from_user.id,
                "Проанализируем лицо на изображении. Прикрепи фотографию, на которой лишь _1 человек_",
                parse_mode="Markdown"
            )


    # Получить текстовое сообщение
    def get_text_message(self, message):
        self.bot.send_message(
            message.from_user.id,
            "Напиши /start",
            parse_mode="Markdown"
        )


    # Получить фото
    def get_photo_messages(self, message):
        try:
            file_info = self.bot.get_file(message.photo[len(message.photo) - 1].file_id)
            full_src = self.get_file(file_info, message)
            self.check_find(full_src, message)
        except Exception as ex: 
            if "full_src" in locals(): Path(full_src).unlink()
            self.send_exception(message, ex)


    # Получить файл
    def get_document_messages(self, message):
        try:
            file_info = self.bot.get_file(message.document.file_id)

            full_src = self.get_file(file_info, message)
            self.check_find(full_src, message)
        except Exception as ex:
            Path(full_src).unlink()
            self.send_exception(message, ex)


    def get_file(self, file_info, message):
        downloaded_file = self.bot.download_file(file_info.file_path)

        full_src = ""
        try: 
            user = user_state[message.from_user.id]
            if user.call_data == {}: raise

            if user.call_data == "face_find":
                full_src = "./storage/saved_photos/"
            full_src += uuid.uuid1().hex[:10] + Path(file_info.file_path).suffix            
        except Exception as ex:
            raise Exception("Зачем ты мне это скинул? Напиши /start")
        
        with Path(full_src).open('wb') as new_file:
            new_file.write(downloaded_file)

        return full_src
    

    def check_find(self, full_src, message):
        try: 
            user = user_state[message.from_user.id]
        except Exception as ex:
            raise Exception("А зачем мне это? Напиши /start")
        
        self.bot.reply_to(message, "Принял. Мне нужно подумать...")
        
        if user.call_data == "get_emotions":
            res = self.deep_face_controller.face_analyze(full_src)[0]
            age = res["age"]
            gender = res["dominant_gender"]
            emotion = res["dominant_emotion"]

            self.bot.send_message(
                message.from_user.id,
                f"Я думаю, что ваш пол *{genders[gender]}* и вам *{age}* лет. Полагаю, ваша эмоция: {emotion}",
                parse_mode="Markdown"
            )

    # Для отправки ошибок
    def send_exception(self, message, exception):
        self.bot.send_message(
            message.from_user.id,
            f"*Ошибка:* {exception}",
            parse_mode="Markdown"
        )


    # Начало работы бота
    def start(self):
        self.bot.polling(none_stop=True)