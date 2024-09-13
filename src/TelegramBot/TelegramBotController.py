import os
import uuid
from pathlib import Path

# Контроллер для управления ботом
class TelegramBotController:
    def __init__(self, bot, deep_face_controller):
        self.bot = bot
        self.deep_face_controller = deep_face_controller
        self.register_handlers()

    # Регистрация всего на свете
    def register_handlers(self):
        self.bot.message_handler(content_types=["text"])(self.get_text_message)
        self.bot.message_handler(content_types=["photo"])(self.get_photo_messages)
        self.bot.message_handler(content_types=["document"])(self.get_file_messages)

    # Получить текстовое сообщение
    def get_text_message(self, message):
        self.bot.send_message(message.from_user.id, "Прикрепи фотографию для того, чтобы я нашел совпадения")

    # Получить фото
    def get_photo_messages(self, message):
        try:
            file_info = self.bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)

            full_src = "./saved_photos/" + uuid.uuid1().hex[:10] + Path(file_info.file_path).suffix

            with Path(full_src).open('wb') as new_file:
                new_file.write(downloaded_file)

            res = self.deep_face_controller.face_find(full_src, "./saved_photos")
            for value in res:
                self.bot.send_photo(
                    message.chat.id,
                    open(value["photo_path"], "rb"),
                    caption=f"Сходство: {value["diff"]}%"
                )

            self.bot.reply_to(message, "Сохранили")
        except Exception as ex: self.send_exception(message, ex)

    # Получить файл
    def get_file_messages(self, message):
        try:
            file_info = self.bot.get_file(message.document.file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)

            full_src = "./saved_photos/" + uuid.uuid1().hex + message.document.file_name

            with Path(full_src).open('wb') as new_file:
                new_file.write(downloaded_file)

            self.bot.reply_to(message, "Сохранили")
        except Exception as ex: self.send_exception(message, ex)

    # Для отправки ошибок
    def send_exception(self, message, exception):
        self.bot.send_message(message.from_user.id, f"Что-то пошло не так с ошибкой: {exception}")

    # Начало работы бота
    def start(self):
        self.bot.polling(none_stop=True)