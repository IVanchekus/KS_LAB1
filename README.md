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

python main.py
```

В конце необходимо подождать загрузку пакетов нейронки