# Установка проекта

```
git clone https://github.com/IVanchekus/KS_LAB1

cd KS_LAB1

python -m venv appvenv

# Для Linux
source ./appvenv/bin/activate

pip install -r requirements.txt

cp .env.example .env

# Поменяйте значение TELEGRAM_BOT_API на ваш в файле .env

sudo apt update
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
sudo apt install tesseract-ocr-rus
sudo apt install tesseract-ocr-chi-sim
sudo apt install tesseract-ocr-chi-tra
sudo apt install tesseract-ocr-spa
sudo apt install tesseract-ocr-fra
sudo apt install tesseract-ocr-deu

# Установите значение TESSERACT_BIN в .env, если это необходимо 

python main.py
```

В конце необходимо подождать загрузку пакетов нейронки