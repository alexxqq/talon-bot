from datetime import datetime, timedelta
from config import COOKIES, CSRF_TOKEN
from config import CHAT_ID, BOT_TOKEN
from utils import is_sunday_or_monday
from globals_var import script_state
from logger_config import logger
import requests
import time

url_template = "https://eq.hsc.gov.ua/site/stepmap?chdate={chdate}&question_id=55"

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

def process_data():

    while script_state.running:
        logger.info("Starting a new run...")
        start_date = datetime.today()
        valid_days = 0

        while valid_days < 15:
            if not is_sunday_or_monday(start_date):
                chdate = start_date.strftime("%Y-%m-%d")
                url = url_template.format(chdate=chdate)

                try:
                    response = requests.get(url, headers=script_state.headers, verify=False)
                    if response.status_code == 200:
                        data = response.json()
                        if data == []:
                            message = "Credentials are no longer valid. The script will stop now."
                            logger.info(message)
                            send_telegram_message(BOT_TOKEN, CHAT_ID, message)
                            script_state.running = False
                            return
                        filtered_data = [
                            entry for entry in data
                            if entry.get('sts') in [1, 3] and entry.get('id_offices') in [98] # 127 # set regions that needed
                        ]

                        if filtered_data:
                            first_entry = filtered_data[0] 
                            message = (
                                f"Filtered data found for {chdate}:\n"
                                f"Office Name: {first_entry.get('offices_name')}\n"
                                f"Office Address: {first_entry.get('offices_addr')}"
                            )
                            send_telegram_message(BOT_TOKEN, CHAT_ID, message)
                        else:
                            logger.info(f"No relevant data found for {chdate}.")
                    else:
                        logger.error(f"Request failed for {chdate} with status code {response.status_code}")

                except Exception as e:
                    logger.error(f"Error during request: {e}")
                
                valid_days += 1

            start_date += timedelta(days=1)

        logger.info("Run completed. Sleeping...")
        time.sleep(10)
