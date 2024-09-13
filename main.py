import telebot

bot = telebot.TeleBot("7382252794:AAES4Js1asYhOzpAEAwdG7mmmAyWDFVHnnc")

@bot.message_handler(content_types=['text', "document"])
def get_text_messages(message):
    print(message)
    # if message.text == "Привет":
    #     bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    # elif message.text == "/help":
    #     bot.send_message(message.from_user.id, "Напиши привет")
    # else:
    #     bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

    bot.send_message(message.from_user.id, "Меня ща разрабатывают")

    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = "/home/ivan/PROJECTS/DOMASHKA/KOMPZRENIE/lab1/photos/" + message.document.file_name

    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "Сохранили") 


bot.polling(none_stop=True, interval=0)