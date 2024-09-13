import telebot
import os
import uuid

bot = telebot.TeleBot("7382252794:AAES4Js1asYhOzpAEAwdG7mmmAyWDFVHnnc")
src = "/home/ivan/PROJECTS/DOMASHKA/KOMPZRENIE/lab1/saved_photos/"

@bot.message_handler(content_types=["text"])
def get_text_message(message):
    bot.send_message(message.from_user.id, "Тестим")

@bot.message_handler(content_types=["photo"])
def get_photo_messages(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    full_src = src + uuid.uuid1().hex + os.path.basename(file_info.file_path)

    with open(full_src, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "Сохранили") 

@bot.message_handler(content_types=["document"])
def get_file_messages(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    full_src = src + uuid.uuid1().hex + message.document.file_name

    with open(full_src, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "Сохранили") 

bot.polling(none_stop=True, interval=0)