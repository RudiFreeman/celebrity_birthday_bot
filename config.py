from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
KINOPOISK_API_TOKEN = os.getenv("KINOPOISK_API_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
USER_ID = int(os.getenv("USER_ID"))
DB_NAME = os.getenv("DB_NAME")