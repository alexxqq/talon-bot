from mapping import OFFICE_MAPPING, QUESTION_MAPPING
from telegram.ext import ContextTypes
from mongo import MongoUserManager
from tasks import process_data
from telegram import Update
from utils import map_offices
import threading

async def start_script(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username

    user = MongoUserManager.get_or_create_user(user_id, username)
    if not user.get('active', None):
        await update.message.reply_text('Use command /pay to access premium features')
    else:
        if not user.get('running'):
            MongoUserManager.set_running(user_id, True)
            await update.message.reply_text(
                f'Script started.\nOffice IDs: {user.get('offices_ids') if user.get('offices_ids') else 'No ID selected'}\nQuestion type: {user.get('question_type')}'
            )
            threading.Thread(target=process_data, args=(user_id,)).start()
        else:
            await update.message.reply_text('Script is already running.')

async def stop_script(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    user = MongoUserManager.get_or_create_user(user_id, update.effective_user.username)

    if user.get('running'):
        MongoUserManager.set_running(user_id, False)
        await update.message.reply_text('Script stopped.')
    else:
        await update.message.reply_text('Script is not running.')

async def script_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = MongoUserManager.get_or_create_user(user_id, update.effective_user.username)

    status = 'running' if user.get('running') else 'stopped'
    await update.message.reply_text(
        f'Script is currently {status}.\nOffice IDs: {user.get('offices_ids') if user.get('offices_ids') else 'No ID selected'}\nQuestion type: {user.get('question_type')}'
    )

async def update_credentials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = MongoUserManager.get_or_create_user(user_id, update.effective_user.username)

    if len(context.args) == 2:
        cookies, csrf_header = context.args

        MongoUserManager.update_credentials(user_id,cookies,csrf_header)

        await update.message.reply_text("Credentials updated successfully.")
    else:
        await update.message.reply_text(
            "Please provide cookies and csrf header: /update_credentials <cookies> <csrf_token>"
        )

async def update_offices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = MongoUserManager.get_or_create_user(user_id, update.effective_user.username)

    if len(context.args) > 0:
        office_names = context.args

        office_ids = [map_offices(name) for name in office_names]

        MongoUserManager.update_offices(user_id, office_ids)

        await update.message.reply_text(
            f"Office IDs updated: {', '.join(map(str, office_ids))}." if office_ids else "No valid office names were provided."
        )
    else:
        await update.message.reply_text(
            "Please provide at least one office name (4-digit number). Example: /update_offices 0541 6348 1247"
        )

async def update_question_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = MongoUserManager.get_or_create_user(user_id, update.effective_user.username)

    if len(context.args) == 1:
        question_type = context.args[0].lower()
        if question_type not in QUESTION_MAPPING:
            await update.message.reply_text("Invalid question type. Use 'practic' or 'theory'.")
            return

        MongoUserManager.update_question_type(user_id, question_type)
        await update.message.reply_text(f"Question type updated to '{question_type}'.")
    else:
        await update.message.reply_text(
            "Please provide a valid question type. Example: /update_question_type practic or /update_question_type theory"
        )
