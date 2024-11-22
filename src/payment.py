from constants import OFFICE_MAPPING, QUESTION_MAPPING
from telegram import Update, LabeledPrice
from telegram.ext import ContextTypes
from mongo import MongoUserManager
from config import PAYMENT_TOKEN
from fetch import process_data
from utils import map_offices
import threading
import logging

logger = logging.getLogger(__name__)

async def send_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username

    user = MongoUserManager.get_or_create_user(user_id, username)
    if user.get('active', None):
        await update.message.reply_text(f"You already have premium features!")
        return
    chat_id = update.effective_chat.id

    title = "Premium Subscription"
    description = "Subscribe to access bot features"
    payload = f"premium_subscription_{user_id}"
    currency = "USD"
    prices = [LabeledPrice("Premium Access", 500)]

    await context.bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token=PAYMENT_TOKEN,
        currency=currency,
        prices=prices,
        start_parameter="premium-access",
    )

async def pre_checkout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    user_id = update.effective_user.id

    if not query.invoice_payload.startswith("premium_subscription"):
        await query.answer(ok=False, error_message="Invalid payment payload.")
    else:
        await query.answer(ok=True)

async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('successful_payment_callback')
    payment_info = update.message.successful_payment
    user_id = update.effective_user.id

    MongoUserManager.update_user_field(user_id, 'active', True)

    logger.info(f'User {user_id} payed for subscribtion')

    await update.message.reply_text(
        f"Payment successful! Thank you for subscribing to premium features. 🎉"
    )
