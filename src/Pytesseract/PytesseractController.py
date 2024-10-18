import pytesseract
import os
from langdetect import detect_langs
from state.dicts import script_to_lang, lang_to_answer

class PytesseractController:
    def __init__(self, pytesseract_bin):
        if pytesseract_bin: pytesseract.pytesseract.tesseract_cmd = pytesseract_bin

    def text_answer_from_img(self, full_src):
        answer = self.detect_text_from_image(full_src)
        #langs = self.lang_detect(text)
        return {
            "text": answer[0],
            "lang": answer[1]
        }

    def detect_text_from_image(self, full_src):
        try:
            osd = pytesseract.image_to_osd(full_src)
            osd_lines = osd.split('\n')
            script_line = [line for line in osd_lines if line.startswith('Script:')][0]
            script = script_line.split(': ')[1]
            lang_code = script_to_lang.get(script, 'eng')
            custom_config = rf"-l {lang_code}"
            text = pytesseract.image_to_string(full_src, config=custom_config)

            if not text.strip():
                raise Exception("Не удалось распознать текст на изображении")
            
            answer = lang_to_answer[script]

            return [text, answer]
        except Exception as ex:
            raise Exception("На изображении плохо видно буквы")
        
    def lang_detect(self, text):
        try:
            lang = detect_langs(text)
            return lang
        except Exception as ex:
            raise ex
            
