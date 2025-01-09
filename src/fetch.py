from utils import is_sunday_or_monday, get_headers, get_url_template
from constants import QUESTION_MAPPING, WAIT_TIME, FETCH_FREETIMES, ITERATION_WAIT_TIME
from datetime import datetime, timedelta
from mongo import MongoUserManager
from config import BOT_TOKEN
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

def fetch_freetimes(office_id, date_of_admission, question_id, headers):
    url = "https://eq.hsc.gov.ua/site/freetimes"
    payload = {
        "office_id": office_id,
        "date_of_admission": date_of_admission,
        "question_id": question_id,
        "es_date": "",
        "es_time": "",
    }
    headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    response = requests.post(url, data=payload, headers=headers, verify=False)

    return response.json() if response.status_code == 200 else []

def process_filtered_data_with_freetimes(filtered_data, headers, chdate, question_type, BOT_TOKEN, chat_id):
    if filtered_data:
        for entry in filtered_data:
            office_id = entry.get('id_offices')
            office_name = entry.get('offices_name')
            office_address = entry.get('offices_addr')

            freetimes_data = fetch_freetimes(office_id, chdate, question_type, headers)
            
            if freetimes_data.get('rows'):
                freetime_message = "\n".join([f"Time: {item['chtime']}" for item in freetimes_data['rows']])

                message = (
                    f"Filtered data found for {chdate}:\n"
                    f"Office Name: {office_name}\n"
                    f"Office Address: {office_address}\n"
                    f"Available Free Times:\n{freetime_message}"
                )
                send_telegram_message(BOT_TOKEN, chat_id, message)
            else:
                logger.info(f"No free times available for {office_name} on {chdate}.")
    else:
        logger.info(f"No relevant data found for {chdate}.")

def process_filtered_data_without_freetimes(filtered_data, chdate, BOT_TOKEN, chat_id):
    if filtered_data:
        for entry in filtered_data:
            office_name = entry.get('offices_name')
            office_address = entry.get('offices_addr')

            message = (
                f"Filtered data found for {chdate}:\n"
                f"Office Name: {office_name}\n"
                f"Office Address: {office_address}\n"
            )
            send_telegram_message(BOT_TOKEN, chat_id, message)
    else:
        logger.info(f"No relevant data found for {chdate}.")

def process_data(chat_id: int) -> None:
    user = MongoUserManager.get_user(chat_id)
    if not user:
        message = "User not found in the database. Please register using the bot."
        send_telegram_message(BOT_TOKEN, chat_id, message)
        return

    offices_ids = user.get("offices_ids", [])

    headers = get_headers(user.get("cookies"), user.get("csrf_token"))
   
    question_type = QUESTION_MAPPING.get(user.get("question_type", "practic"))

    url_template = get_url_template(question_type)

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

                        if FETCH_FREETIMES:
                            process_filtered_data_with_freetimes(filtered_data, headers, chdate, question_type, BOT_TOKEN, chat_id)
                        else:
                            process_filtered_data_without_freetimes(filtered_data, chdate, BOT_TOKEN, chat_id)
                    else:
                        logger.error(f"Request failed for {chdate} with status code {response.status_code}")

                except Exception as e:
                    logger.error(f"Error during request for {chdate}: {e}")
                    message = "Stopping script, maybe system thought I am a bot or another error, go to site and confirm you are not a bot or contact developer."
                    MongoUserManager.set_running(chat_id, False)
                    send_telegram_message(BOT_TOKEN, chat_id, message)
                    return

                valid_days += 1

            start_date += timedelta(days=1)
            time.sleep(ITERATION_WAIT_TIME)
            if not MongoUserManager.get_running(chat_id):
                return
        logger.info(f"Processing completed for user {chat_id}.")
        time.sleep(WAIT_TIME)