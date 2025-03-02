# config.py
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Telegram-бот
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Google Sheets
GOOGLE_SHEETS_CREDENTIALS_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS_FILE")
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME")


# Расписание рассылки
SCHEDULE_DAY_OF_WEEK = os.getenv("SCHEDULE_DAY_OF_WEEK")
SCHEDULE_HOUR = int(os.getenv("SCHEDULE_HOUR", 9))
SCHEDULE_MINUTE = int(os.getenv("SCHEDULE_MINUTE", 0))

# Администраторы (если несколько, разделяй запятыми)
ADMIN_IDS = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(admin.strip()) for admin in ADMIN_IDS.split(",") if admin.strip()]
# config.py
# Период новостей: брать новости за последние X дней
NEWS_PERIOD_DAYS = 5 # Новости за последние 5 дней

