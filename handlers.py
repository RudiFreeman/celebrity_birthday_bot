# Импортируем необходимые модули для обработки сообщений, кнопок и команд
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand # type: ignore
from telegram.ext import CallbackContext # type: ignore
from modules.celebrity_birthday import create_birthday_post  # Импортируем функцию для поста о знаменитости
from modules.post_manager import post_manager  # Импортируем менеджер постов
import config  # Импортируем настройки

# Асинхронная функция для настройки меню команд
async def setup_commands(bot):
    # Создаем список команд для меню Telegram (только главные команды)
    commands = [
        BotCommand("celebrity_birthday", "Создать пост о дне рождения знаменитости"),
        BotCommand("movie_night", "Выбрать фильм на вечер"),
        BotCommand("movie_news", "Получить новости из мира кино"),
    ]
    # Устанавливаем команды в Telegram
    await bot.set_my_commands(commands)

# Декоратор для ограничения доступа к командам
def restrict_user(handler_func):
    async def wrapper(update: Update, context: CallbackContext):
        if update.effective_user.id == config.USER_ID:
            return await handler_func(update, context)
        else:
            await update.message.reply_text("Эта команда доступна только администратору.")
    return wrapper

# Обработчик команды /start
@restrict_user
async def start(update: Update, context: CallbackContext):
    # Создаем список кнопок для меню
    keyboard = [
        [InlineKeyboardButton("День рождения знаменитости", callback_data='celebrity_birthday')],
        [InlineKeyboardButton("Фильм на вечер", callback_data='movie_night')],
        [InlineKeyboardButton("Новости из мира кино", callback_data='movie_news')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)  # Формируем разметку с кнопками
    
    # Отправляем сообщение с вопросом и прикрепляем кнопки
    await update.message.reply_text('Какой пост вы хотите создать?', reply_markup=reply_markup)

# Обработчик команды /celebrity_birthday
@restrict_user
async def celebrity_birthday(update: Update, context: CallbackContext):
    # Вызываем функцию создания поста о дне рождения
    await create_birthday_post(update, context)

# Обработчик команды /movie_night
@restrict_user
async def movie_night(update: Update, context: CallbackContext):
    # Отвечаем на команду выбора фильма
    await update.message.reply_text('Вы выбрали: Фильм на вечер. Я найду отличный фильм для вас!')

# Обработчик команды /movie_news
@restrict_user
async def movie_news(update: Update, context: CallbackContext):
    # Отвечаем на команду новостей
    await update.message.reply_text('Вы выбрали: Новости из мира кино. Сейчас соберу последние новости!')

# Обработчик команды /edit_text
@restrict_user
async def edit_text(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Укажите новый текст: /edit_text [новый текст]")
        return
    new_text = " ".join(context.args)
    await post_manager.edit_post_text(update, context, new_text)

# Обработчик команды /edit_image
@restrict_user
async def edit_image(update: Update, context: CallbackContext):
    if not context.args:
        await update.message.reply_text("Укажите URL изображения: /edit_image [URL]")
        return
    new_image_url = context.args[0]
    await post_manager.edit_post_image(update, context, new_image_url)

# Обработчик загруженных фотографий
@restrict_user
async def handle_photo(update: Update, context: CallbackContext):
    if context.user_data.get('awaiting_image'):
        # Получаем файл фотографии
        photo = update.message.photo[-1]  # Берем фото наивысшего качества
        file = await photo.get_file()
        file_url = file.file_path
        
        # Обновляем пост с новым изображением
        await post_manager.edit_post_image(update, context, file_url)
        
        # Сбрасываем состояние ожидания изображения
        context.user_data['awaiting_image'] = False
    else:
        await update.message.reply_text("Пожалуйста, сначала нажмите 'Редактировать изображение'.")

# Обработчик команды /schedule
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

# Обработчик команды /reset
@restrict_user
async def reset(update: Update, context: CallbackContext):
    await post_manager.reset_post(update, context)

# Обработчик команды /send_now
@restrict_user
async def send_now(update: Update, context: CallbackContext):
    await post_manager.send_post_now(update, context)

# Обработчик нажатий на кнопки
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query  # Получаем данные о нажатии кнопки
    await query.answer()  # Подтверждаем, что нажатие обработано
    
    # Проверяем, что пользователь — администратор
    if query.from_user.id != config.USER_ID:
        await query.message.reply_text("Эта функция доступна только администратору.")
        return
    
    # Обрабатываем нажатия на кнопки
    if query.data == 'celebrity_birthday':
        # Вызываем функцию создания поста о дне рождения
        await create_birthday_post(query, context)
    elif query.data == 'movie_night':
        # Отвечаем, если выбрано "Фильм на вечер"
        await query.message.reply_text('Вы выбрали: Фильм на вечер. Я найду отличный фильм для вас!')
    elif query.data == 'movie_news':
        # Отвечаем, если выбрано "Новости из мира кино"
        await query.message.reply_text('Вы выбрали: Новости из мира кино. Сейчас соберу последние новости!')
    elif query.data == 'edit_text':
        # Запрашиваем новый текст
        await query.message.reply_text("Отправьте новый текст для поста с помощью /edit_text [текст]")
    elif query.data == 'edit_image':
        # Запрашиваем URL или изображение
        await query.message.reply_text("Отправьте URL изображения (/edit_image [URL]) или загрузите фотографию.")
        context.user_data['awaiting_image'] = True  # Устанавливаем состояние ожидания изображения
    elif query.data == 'schedule':
        # Запрашиваем время для планирования
        await query.message.reply_text("Укажите время публикации с помощью /schedule [час] [минута]")
    elif query.data == 'reset':
        # Сбрасываем пост
        await post_manager.reset_post(update, context)
    elif query.data == 'send_now':
        # Отправляем пост сразу
        await post_manager.send_post_now(update, context)

# Обработчик текстовых сообщений (кроме команд)
async def echo(update: Update, context: CallbackContext):
    # Повторяем текст, который отправил пользователь
    await update.message.reply_text(f'Боту сказали: {update.message.text}')