import pytesseract
import os
from langdetect import detect_langs
from state.dicts import script_to_lang

class PytesseractController:
    def __init__(self, pytesseract_bin):
        if pytesseract_bin: pytesseract.pytesseract.tesseract_cmd = pytesseract_bin

    def text_answer_from_img(self, full_src):
        text = self.detect_text_from_image(full_src)
        langs = self.lang_detect(text)
        return {
            "text": text,
            "langs": langs
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
            
            return text
        except Exception as ex:
            raise ex
        
    def lang_detect(self, text):
        try:
            lang = detect_langs(text)
            return lang
        except Exception as ex:
            raise ex
            
