from datetime import datetime, timedelta
from config import BOT_TOKEN
from utils import is_sunday_or_monday
from mongo import MongoUserManager
from mapping import QUESTION_MAPPING
import requests
import logging
import time

logger = logging.getLogger(__name__)

def send_telegram_message(bot_token, chat_id, message):
    """Send a message to the specified Telegram chat."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            logger.info("Message sent successfully.")
        else:
            logger.info(f"Failed to send message: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Error while sending message: {e}")

def process_data(chat_id: int) -> None:
    user = MongoUserManager.get_user(chat_id)
    if not user:
        message = "User not found in the database. Please register using the bot."
        logger.info(message)
        send_telegram_message(BOT_TOKEN, chat_id, message)
        return

    offices_ids = user.get("offices_ids", [])
    headers = {
        "cookie": user.get("cookies"),
        "x-csrf-token": user.get("csrf_token"),
        "referer": "https://eq.hsc.gov.ua/site/step2?chdate=2024-10-11&question_id=55&id_es=",
    }
    question_type = QUESTION_MAPPING.get(user.get("question_type", "practic"))

    url_template = f"https://eq.hsc.gov.ua/site/stepmap?chdate={{chdate}}&question_id={question_type}"

    if not offices_ids:
        MongoUserManager.set_running(chat_id, False)
        message = "No offices selected. Please update offices using the /update_offices command."
        logger.info(message)
        send_telegram_message(BOT_TOKEN, chat_id, message)
        return
    
    while MongoUserManager.get_running(chat_id):
        logger.info(f"Starting process for user {chat_id}.")
        start_date = datetime.today()
        valid_days = 0
        while valid_days < 15:
            if not is_sunday_or_monday(start_date):
                chdate = start_date.strftime("%Y-%m-%d")
                url = url_template.format(chdate=chdate)

                try:
                    response = requests.get(url, headers=headers, verify=False)
                    if response.status_code == 200:
                        data = response.json()

                        if not data:
                            message = "Credentials are invalid or expired. Please update them using the /update_credentials command."
                            logger.info(message)
                            send_telegram_message(BOT_TOKEN, chat_id, message)
                            MongoUserManager.set_running(chat_id, False)
                            return

                        filtered_data = [
                            entry for entry in data
                            if entry.get("sts") in [1, 3] and entry.get("id_offices") in offices_ids
                        ]

                        if filtered_data:
                            first_entry = filtered_data[0] 
                            message = (
                                f"Filtered data found for {chdate}:\n"
                                f"Office Name: {first_entry.get('offices_name')}\n"
                                f"Office Address: {first_entry.get('offices_addr')}"
                            )
                            send_telegram_message(BOT_TOKEN, chat_id, message)
                        else:
                            logger.info(f"No relevant data found for {chdate}.")
                    else:
                        logger.error(f"Request failed for {chdate} with status code {response.status_code}")

                except Exception as e:
                    logger.error(f"Error during request for {chdate}: {e}")

                valid_days += 1

            start_date += timedelta(days=1)

        logger.info(f"Processing completed for user {chat_id}.")
        time.sleep(10)