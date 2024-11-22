from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_PASS = os.getenv("MONGO_PASS")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_HOST = os.getenv("MONGO_HOST")
PAYMENT_TOKEN = os.getenv("PAYMENT_TOKEN")
