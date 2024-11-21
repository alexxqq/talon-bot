from telegram.ext import ContextTypes
from globals_var import script_state
from tasks import process_data
from telegram import Update
import threading

async def start_script(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    if not script_state.running:
        script_state.running = True
        await update.message.reply_text(f"Script started.\nOffice id's: {script_state.offices_ids if script_state.offices_ids else 'No id selected'}")

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
    await update.message.reply_text(f"Script is currently {status}.\nOffice id's: {script_state.offices_ids if script_state.offices_ids else 'No id selected'}\nQuestion type: {script_state.current_question_type}")

async def update_credentials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
     if len(context.args) == 3:
        new_webchsid2 = context.args[0]
        new__csrf = context.args[1]
        new_csrf_token = context.args[2]

        script_state.update_cookies_and_header(new_webchsid2, new__csrf, new_csrf_token)

        await update.message.reply_text("Credentials updated successfully.")
     else:
        await update.message.reply_text("Please provide WEBCHSID2, _csrf, and csrf token for the header. Example: /update_credentials <WEBCHSID2> <_csrf> <csrf_token>")

async def update_offices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) > 0:
        office_names = context.args

        script_state.update_offices(office_names)

        if script_state.offices_ids:
            await update.message.reply_text(f"Office IDs updated: {', '.join(map(str, script_state.offices_ids))}.")
        else:
            await update.message.reply_text("No valid office names were provided.")
    else:
        await update.message.reply_text("Please provide at least one office name (4-digit number). Example: /update_offices 0541 6348 1247")

async def update_question_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 1:
        question_type = context.args[0].lower()

        try:
            script_state.update_question_type(question_type)
            await update.message.reply_text(f"Question type updated to '{question_type}'.")
        except ValueError as e:
            await update.message.reply_text(str(e))
    else:
        await update.message.reply_text("Please provide a valid question type. Example: /update_question_type practic or /update_question_type theory")
