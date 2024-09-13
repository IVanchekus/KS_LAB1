import os
import uuid
from pathlib import Path

# Контроллер для управления ботом
class TelegramBotController:
    def __init__(self, bot):
        self.bot = bot
        self.register_handlers()

    def register_handlers(self):
        self.bot.message_handler(content_types=["text"])(self.get_text_message)
        self.bot.message_handler(content_types=["photo"])(self.get_photo_messages)
        self.bot.message_handler(content_types=["document"])(self.get_file_messages)

    def get_text_message(self, message):
        self.bot.send_message(message.from_user.id, "Прикрепи фотографию для того, чтобы я нашел совпадения")

    def get_photo_messages(self, message):
        file_info = self.bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = self.bot.download_file(file_info.file_path)

        full_src = "./saved_photos/" + uuid.uuid1().hex + os.path.basename(file_info.file_path)

        with Path(full_src).open('wb') as new_file:
            new_file.write(downloaded_file)

        self.bot.reply_to(message, "Сохранили")

    def get_file_messages(self, message):
        file_info = self.bot.get_file(message.document.file_id)
        downloaded_file = self.bot.download_file(file_info.file_path)

        full_src = "./saved_photos/" + uuid.uuid1().hex + message.document.file_name

        with Path(full_src).open('wb') as new_file:
            new_file.write(downloaded_file)

        self.bot.reply_to(message, "Сохранили")

    def start(self):
        self.bot.polling(none_stop=True)