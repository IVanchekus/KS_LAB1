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
    def __init__(self, bot, deep_face_controller, pytesseract_contoller, yolo_controller):
        self.bot = bot
        self.deep_face_controller = deep_face_controller
        self.pytesseract_contoller = pytesseract_contoller
        self.yolo_controller = yolo_controller
        self.register_handlers()


    # Регистрация всего на свете
    def register_handlers(self):
        self.bot.message_handler(commands=["start"])(self.start_command)
        self.bot.callback_query_handler(func=lambda call: True)(self.callback_query)
        self.bot.message_handler(content_types=["text"])(self.get_text_message)
        self.bot.message_handler(content_types=["photo"])(self.get_photo_messages)
        self.bot.message_handler(content_types=["document"])(self.get_document_messages)
        self.bot.message_handler(content_types=["video"])(self.get_video_message)

    def start_command(self, message): # TODO поменять функцию
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton("Поиск похожих людей", callback_data="face_find")
        button2 = types.InlineKeyboardButton("Получить приколюшку", callback_data="get_meme")
        button3 = types.InlineKeyboardButton("Получить текст из изображения", callback_data="text_image")
        button4 = types.InlineKeyboardButton("Найти объекты в видео", callback_data="video_detector")
        keyboard.add(button1, button2, button3, button4)
        
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
        elif call.data == "text_image":
            self.bot.send_message(
                call.from_user.id,
                "Найдем текст по фотографии. Прикрепи фотографию, на которой есть текст",
                parse_mode="Markdown"
            )
        elif call.data == "video_detector":
            self.bot.send_message(
                call.from_user.id,
                "Найдем объекты в видео. Прикрепи видео, в котором хочешь найти объекты",
                parse_mode="Markdown"
            )

    # Получить видео
    def get_video_message(self, message):
        try:
            file_info = self.bot.get_file(message.video.file_id)
            full_src = self.get_file(file_info, message)
            self.check_find(full_src, message)
        except Exception as ex:
            Path(full_src).unlink()
            self.send_exception(message, ex)


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

            if user.call_data == "text_image":
                full_src = "./storage/temp/"
            elif user.call_data == "face_find":
                full_src = "./storage/saved_photos/"
            elif user.call_data == "video_detector":
                full_src = "./storage/videos/"
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
            res = self.deep_face_controller.face_analyze(full_src)[0]
            age = res["age"]
            gender = res["dominant_gender"]

            self.bot.send_message(
                message.from_user.id,
                f"Я думаю, что ваш пол *{genders[gender]}* и вам *{age} лет*. Давайте подберу вам приколюшку!",
                parse_mode="Markdown"
            )
            self.send_meme(message, (gender, age), full_src)
        elif user.call_data == "text_image":
            res = self.pytesseract_contoller.text_answer_from_img(full_src)

            self.bot.send_message(
                message.from_user.id,   
                f"*{res['lang']}:* \n{res['text']}",
                parse_mode="Markdown"
            )
            Path(full_src).unlink()
        elif user.call_data == "video_detector":
            res = self.yolo_controller.process_video(full_src)

            self.bot.send_message(
                message.from_user.id,   
                self.yolo_controller.send_detected_objects_message(res),
                parse_mode="Markdown"
            )
            Path(full_src).unlink()


    def send_meme(self, message, user_info, full_src):
        text, age_interval = self.message_from_gender_age(*user_info)
        # Отправить приветственное сообщение
        self.bot.send_message(
            message.from_user.id,
            text
        )

        # Отправить рандомный мем по возрасту
        self.bot.send_photo(
            message.from_user.id,
            open(self.random_meme_from_gender_age(*user_info, age_interval, full_src), "rb")
        )


    def message_from_gender_age(self, gender, age):
        text = ''
        age_interval = ''
        if age < 18:
            text += "Привет, " + ("юный джентельмен!" if gender == "Man" else "юная леди!")
            age_interval = '18'
        elif age in range(18, 30):
            text += "Здравствуй, " + ("молодой человек!" if gender == "Man" else "молодая девушка!")
            age_interval = '18-30'
        elif age in range(30, 40):
            text += "Приветствую, " + ("уважаемый мужчина!" if gender == "Man" else "уважаемая женщина!")
            age_interval = '30-40'
        elif age >= 40:
            text += "Добрый день, " + ("опыйтный джентельмен!" if gender == "Man" else "опытная леди!")
            age_interval = '40'
        return text, age_interval
    
    def random_meme_from_gender_age(self, gender, age, age_interval, full_src):
        src = Path(f"./storage/memes/{age_interval}/{gender}")
        files = list(src.iterdir())
        image_ext = {'.jpg', '.jpeg', '.png'}
        image_files = [f for f in files if f.is_file() and f.suffix.lower() in image_ext]

        dominant_color_full_src = self.check_dominant_color(full_src)
        distance = 0
        exit_image = ''
        for image in image_files:
            dominant_color_image = self.check_dominant_color(image)
            new_distance = self.euclidean_distance(dominant_color_full_src, dominant_color_image)
            if distance < new_distance:
                distance = new_distance
                exit_image = image

        return exit_image
    
    def euclidean_distance(self, point1, point2):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1, point2)))
    
    def check_dominant_color(self, image):
        color_thief = ColorThief(image)
        dominant_color = color_thief.get_color(quality=1)
        return dominant_color

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