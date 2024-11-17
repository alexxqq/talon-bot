from commands import start_script, stop_script, script_status, update_credentials
from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from telegram import Update
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start_script", start_script))
    application.add_handler(CommandHandler("stop_script", stop_script))
    application.add_handler(CommandHandler("script_status", script_status))
    application.add_handler(CommandHandler("update_credentials", update_credentials))

    application.run_polling()

if __name__ == "__main__":
    main()
