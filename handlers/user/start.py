from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import CallbackContext
import config

async def setup_commands(bot):
    commands = [
        BotCommand("celebrity_birthday", "Создать пост о дне рождения знаменитости"),
        BotCommand("movie_night", "Выбрать фильм на вечер"),
        BotCommand("movie_news", "Получить новости из мира кино"),
    ]
    await bot.set_my_commands(commands)

def restrict_user(handler_func):
    async def wrapper(update: Update, context: CallbackContext):
        if update.effective_user.id == config.USER_ID:
            return await handler_func(update, context)
        await update.message.reply_text("Эта команда доступна только администратору.")
    return wrapper

@restrict_user
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("День рождения знаменитости", callback_data='celebrity_birthday')],
        [InlineKeyboardButton("Фильм на вечер", callback_data='movie_night')],
        [InlineKeyboardButton("Новости из мира кино", callback_data='movie_news')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Какой пост вы хотите создать?', reply_markup=reply_markup)