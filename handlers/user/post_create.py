from telegram import Update
from telegram.ext import CallbackContext
from modules.celebrity_birthday import create_birthday_post
import config

def restrict_user(handler_func):
    async def wrapper(update: Update, context: CallbackContext):
        if update.effective_user.id == config.USER_ID:
            return await handler_func(update, context)
        await update.message.reply_text("Эта команда доступна только администратору.")
    return wrapper

@restrict_user
async def celebrity_birthday(update: Update, context: CallbackContext):
    await create_birthday_post(update, context)

@restrict_user
async def movie_night(update: Update, context: CallbackContext):
    await update.message.reply_text('Вы выбрали: Фильм на вечер. Я найду отличный фильм для вас!')

@restrict_user
async def movie_news(update: Update, context: CallbackContext):
    await update.message.reply_text('Вы выбрали: Новости из мира кино. Сейчас соберу последние новости!')