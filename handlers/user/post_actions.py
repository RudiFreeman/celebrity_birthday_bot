from telegram import Update
from telegram.ext import CallbackContext
from modules.post_manager import post_manager
from modules.celebrity_birthday import create_birthday_post
import config

def restrict_user(handler_func):
    async def wrapper(update: Update, context: CallbackContext):
        if update.effective_user.id == config.USER_ID:
            return await handler_func(update, context)
        await update.message.reply_text("Эта команда доступна только администратору.")
    return wrapper

@restrict_user
async def edit_text(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Укажите новый текст: /edit_text [новый текст]")
        return
    new_text = " ".join(context.args)
    await post_manager.edit_post_text(update, context, new_text)

@restrict_user
async def edit_image(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Укажите URL изображения: /edit_image [URL]")
        return
    new_image_url = context.args[0]
    await post_manager.edit_post_image(update, context, new_image_url)

@restrict_user
async def handle_photo(update: Update, context: CallbackContext):
    if context.user_data.get('awaiting_image'):
        photo = update.message.photo[-1]
        file = await photo.get_file()
        file_url = file.file_path
        await post_manager.edit_post_image(update, context, file_url)
        context.user_data['awaiting_image'] = False
    else:
        await update.message.reply_text("Пожалуйста, сначала нажмите 'Редактировать изображение'.")

@restrict_user
async def schedule(update: Update, context: CallbackContext):
    if not context.args or len(context.args) != 2:
        await update.message.reply_text("Укажите время: /schedule [час] [минута]")
        return
    try:
        hour, minute = map(int, context.args)
        await post_manager.schedule_post(update, context, hour, minute)
    except ValueError:
        await update.message.reply_text("Укажите корректное время: /schedule [час] [минута]")

@restrict_user
async def reset(update: Update, context: CallbackContext):
    await post_manager.reset_post(update, context)

@restrict_user
async def send_now(update: Update, context: CallbackContext):
    await post_manager.send_post_now(update, context)

async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    if query.from_user.id != config.USER_ID:
        await query.message.reply_text("Эта функция доступна только администратору.")
        return
    if query.data == 'celebrity_birthday':
        await create_birthday_post(query, context)
    elif query.data == 'movie_night':
        await query.message.reply_text('Вы выбрали: Фильм на вечер. Я найду отличный фильм для вас!')
    elif query.data == 'movie_news':
        await query.message.reply_text('Вы выбрали: Новости из мира кино. Сейчас соберу последние новости!')
    elif query.data == 'edit_text':
        await query.message.reply_text("Отправьте новый текст для поста с помощью /edit_text [текст]")
    elif query.data == 'edit_image':
        await query.message.reply_text("Отправьте URL изображения (/edit_image [URL]) или загрузите фотографию.")
        context.user_data['awaiting_image'] = True
    elif query.data == 'schedule':
        await query.message.reply_text("Укажите время публикации с помощью /schedule [час] [минута]")
    elif query.data == 'reset':
        await post_manager.reset_post(update, context)
    elif query.data == 'send_now':
        await post_manager.send_post_now(update, context)