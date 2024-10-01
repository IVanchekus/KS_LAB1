import uuid
from pathlib import Path
from telebot import types
from addict import Dict
from state.state import user_state

# Контроллер для управления ботом
class TelegramBotController:
    def __init__(self, bot, deep_face_controller):
        self.bot = bot
        self.deep_face_controller = deep_face_controller
        self.register_handlers()


    # Регистрация всего на свете
    def register_handlers(self):
        self.bot.message_handler(commands=["start"])(self.startBot)
        self.bot.callback_query_handler(func=lambda call: True)(self.callback_query)
        self.bot.message_handler(content_types=["text"])(self.get_text_message)
        self.bot.message_handler(content_types=["photo"])(self.get_photo_messages)
        self.bot.message_handler(content_types=["document"])(self.get_document_messages)


    def startBot(self, message): # TODO поменять функцию
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Поиск похожих людей", callback_data="face_find")
        button2 = types.InlineKeyboardButton("Получить приколюшку", callback_data="get_meme")
        keyboard.add(button1, button2)
        
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
        if call.data == "face_find":
            self.bot.send_message(
                call.from_user.id,
                "Найдем похожих людей. Прикрепи фотографию, на которой лишь _1 человек_",
                parse_mode="Markdown"
            )
        elif call.data == "get_meme":
            self.bot.send_message(
                call.from_user.id,
                "Найдем мем по фотографии. Прикрепи фотографию, на которой лишь _1 человек_",
                parse_mode="Markdown"
            )


    # Получить текстовое сообщение
    def get_text_message(self, message):
        self.bot.send_message(
            message.from_user.id,
            "Прикрепи фотографию, на которой лишь _1 человек_",
            parse_mode="Markdown"
        )


    # Получить фото
    def get_photo_messages(self, message):
        try:
            file_info = self.bot.get_file(message.photo[len(message.photo) - 1].file_id)

            full_src = self.get_file(file_info)
            self.check_find(full_src, message)

            self.bot.reply_to(message, "Сохранили")
        except Exception as ex: 
            Path(full_src).unlink()
            self.send_exception(message, ex)


    # Получить файл
    def get_document_messages(self, message):
        try:
            file_info = self.bot.get_file(message.document.file_id)

            full_src = self.get_file(file_info)
            self.check_find(full_src, message)

            self.bot.reply_to(message, "Сохранили")
        except Exception as ex:
            Path(full_src).unlink()
            self.send_exception(message, ex)


    def get_file(self, file_info):
        downloaded_file = self.bot.download_file(file_info.file_path)

        full_src = "./storage/saved_photos/" + uuid.uuid1().hex[:10] + Path(file_info.file_path).suffix

        with Path(full_src).open('wb') as new_file:
            new_file.write(downloaded_file)

        return full_src
    

    def check_find(self, full_src, message):
        try: 
            user = user_state[message.from_user.id]

            if user.call_data == "face_find":
                res = self.deep_face_controller.face_find(full_src, "./storage/saved_photos")

                if len(res) == 0: self.bot.send_message(message.from_user.id, "Не нашел схожих лиц. Попробуй еще раз!")

                for value in res:
                    self.bot.send_photo(
                        message.chat.id,
                        open(value["photo_path"], "rb"),
                        caption=f"Сходство: {value['diff']}%"
                    )
            elif user.call_data == "get_meme":
                res = self.deep_face_controller.face_analyze(full_src)
                self.bot.send_message(
                    message.from_user.id,
                    f"{res}"
                )

        except Exception as ex:
            raise Exception("А зачем мне эта фотка? Напиши /start")


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