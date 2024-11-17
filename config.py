from dotenv import load_dotenv
import os

load_dotenv()

CHAT_ID = os.getenv("CHAT_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
COOKIES = os.getenv("COOKIES")
CSRF_TOKEN = os.getenv("CSRF_TOKEN")
