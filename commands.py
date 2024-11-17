from telegram.ext import ContextTypes
from globals_var import script_state
from tasks import process_data
from telegram import Update
import threading

async def start_script(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if not script_state.running:
        script_state.running = True
        await update.message.reply_text("Script started.")

        threading.Thread(target=process_data).start()
    else:
        await update.message.reply_text("Script is already running.")

async def stop_script(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if script_state.running:
        script_state.running = False
        await update.message.reply_text("Script stopped.")
    else:
        await update.message.reply_text("Script is not running.")

async def script_status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    status = "running" if script_state.running else "stopped"
    await update.message.reply_text(f"Script is currently {status}.")

async def update_credentials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
     if len(context.args) == 3:
        new_webchsid2 = context.args[0]
        new__csrf = context.args[1]
        new_csrf_token = context.args[2]

        script_state.update_cookies_and_header(new_webchsid2, new__csrf, new_csrf_token)

        await update.message.reply_text("Credentials updated successfully.")
     else:
        await update.message.reply_text("Please provide WEBCHSID2, _csrf, and csrf token for the header. Example: /update_credentials <WEBCHSID2> <_csrf> <csrf_token>")