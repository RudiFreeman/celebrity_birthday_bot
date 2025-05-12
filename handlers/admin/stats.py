from telegram import Update
from telegram.ext import CallbackContext

async def stats(update: Update, context: CallbackContext):
    await update.message.reply_text("Статистика пока недоступна.")