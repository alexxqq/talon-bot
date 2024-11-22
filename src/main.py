from commands import start_script, stop_script, script_status, update_credentials, update_offices, update_question_type
from telegram.ext import Application, CommandHandler, PreCheckoutQueryHandler, MessageHandler,filters
from payment import send_invoice, pre_checkout_callback, successful_payment_callback
from config import BOT_TOKEN
import urllib3
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start_script", start_script))
    application.add_handler(CommandHandler("stop_script", stop_script))
    application.add_handler(CommandHandler("script_status", script_status))
    application.add_handler(CommandHandler("update_credentials", update_credentials))
    application.add_handler(CommandHandler("update_offices", update_offices))
    application.add_handler(CommandHandler("update_question_type", update_question_type))


    application.add_handler(CommandHandler("pay", send_invoice))
    application.add_handler(PreCheckoutQueryHandler(pre_checkout_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback))


    application.run_polling()

if __name__ == "__main__":
    main()
