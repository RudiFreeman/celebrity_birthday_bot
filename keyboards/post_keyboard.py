from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_post_management_keyboard():
    keyboard = [
        [InlineKeyboardButton("Отправить сейчас", callback_data='send_now')],
        [InlineKeyboardButton("Запланировать публикацию", callback_data='schedule')],
        [InlineKeyboardButton("Сбросить пост", callback_data='reset')],
        [InlineKeyboardButton("Редактировать текст", callback_data='edit_text')],
        [InlineKeyboardButton("Редактировать изображение", callback_data='edit_image')],
    ]
    return InlineKeyboardMarkup(keyboard)