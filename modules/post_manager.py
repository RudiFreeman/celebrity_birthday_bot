# Импортируем необходимые модули
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup # type: ignore
from telegram.ext import CallbackContext # type: ignore
import config  # Импортируем настройки
from apscheduler.schedulers.background import BackgroundScheduler # type: ignore
from datetime import datetime

# Класс для управления постами
class PostManager:
    def __init__(self):
        self.current_post = None  # Хранит данные последнего поста
        self.scheduler = BackgroundScheduler()  # Планировщик для публикаций
        self.scheduler.start()  # Запускаем планировщик

    # Вспомогательная функция для отправки кнопок управления
    async def _send_management_buttons(self, context: CallbackContext, chat_id: int):
        keyboard = [
            [InlineKeyboardButton("Отправить сейчас", callback_data='send_now')],
            [InlineKeyboardButton("Запланировать публикацию", callback_data='schedule')],
            [InlineKeyboardButton("Сбросить пост", callback_data='reset')],
            [InlineKeyboardButton("Редактировать текст", callback_data='edit_text')],
            [InlineKeyboardButton("Редактировать изображение", callback_data='edit_image')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    # await context.bot.send_message(chat_id=chat_id, text="Управляйте постом:", reply_markup=reply_markup)

    # Функция для отправки поста
    async def send_post(self, update: Update, context: CallbackContext, text: str, image_url: str = None):
        chat_id = update.effective_chat.id
        if image_url:
            message = await context.bot.send_photo(chat_id=chat_id, photo=image_url, caption=text)
        else:
            message = await context.bot.send_message(chat_id=chat_id, text=text)
        
        # Сохраняем данные поста
        self.current_post = {
            'chat_id': chat_id,
            'message_id': message.message_id,
            'text': text,
            'image_url': image_url
        }
        
        # Отправляем кнопки управления
        await self._send_management_buttons(context, chat_id)

    # Функция для редактирования текста поста
    async def edit_post_text(self, update: Update, context: CallbackContext, new_text: str):
        if not self.current_post:
            await update.message.reply_text("Нет активного поста для редактирования.")
            return
        
        # Обновляем текст поста
        self.current_post['text'] = new_text
        if self.current_post['image_url']:
            await context.bot.edit_message_caption(
                chat_id=self.current_post['chat_id'],
                message_id=self.current_post['message_id'],
                caption=new_text
            )
        else:
            await context.bot.edit_message_text(
                chat_id=self.current_post['chat_id'],
                message_id=self.current_post['message_id'],
                text=new_text
            )
        await update.message.reply_text("Текст поста обновлён.")
        # Отправляем кнопки управления
        await self._send_management_buttons(context, self.current_post['chat_id'])

    # Функция для редактирования изображения поста
    async def edit_post_image(self, update: Update, context: CallbackContext, new_image_url: str):
        if not self.current_post:
            await update.message.reply_text("Нет активного поста для редактирования.")
            return
        
        # Обновляем изображение
        self.current_post['image_url'] = new_image_url
        # Удаляем старое сообщение
        await context.bot.delete_message(
            chat_id=self.current_post['chat_id'],
            message_id=self.current_post['message_id']
        )
        # Отправляем новое сообщение с изображением и текстом
        message = await context.bot.send_photo(
            chat_id=self.current_post['chat_id'],
            photo=new_image_url,
            caption=self.current_post['text']
        )
        self.current_post['message_id'] = message.message_id
        await update.message.reply_text("Изображение поста обновлено.")
        # Отправляем кнопки управления
        await self._send_management_buttons(context, self.current_post['chat_id'])

    # Функция для планирования публикации
    async def schedule_post(self, update: Update, context: CallbackContext, hour: int, minute: int):
        if not self.current_post:
            await update.callback_query.message.reply_text("Нет активного поста для планирования.")
            return
        
        # Планируем отправку в канал
        def job():
            context.bot.send_message(
                chat_id=config.CHANNEL_ID,
                text=self.current_post['text']
            ) if not self.current_post['image_url'] else context.bot.send_photo(
                chat_id=config.CHANNEL_ID,
                photo=self.current_post['image_url'],
                caption=self.current_post['text']
            )
            self.current_post = None  # Сбрасываем пост после отправки
        
        self.scheduler.add_job(job, 'cron', hour=hour, minute=minute)
        await update.callback_query.message.reply_text(f"Пост запланирован на {hour:02d}:{minute:02d}.")
        # Отправляем кнопки управления
        await self._send_management_buttons(context, self.current_post['chat_id'])

    # Функция для сброса поста
    async def reset_post(self, update: Update, context: CallbackContext):
        if not self.current_post:
            await update.callback_query.message.reply_text("Нет активного поста для сброса.")
            return
        self.current_post = None
        await update.callback_query.message.reply_text("Пост сброшён.")
        # Отправляем меню выбора действия
        keyboard = [
            [InlineKeyboardButton("День рождения знаменитости", callback_data='celebrity_birthday')],
            [InlineKeyboardButton("Фильм на вечер", callback_data='movie_night')],
            [InlineKeyboardButton("Новости из мира кино", callback_data='movie_news')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Какой пост вы хотите создать?",
            reply_markup=reply_markup
        )

    # Функция для немедленной отправки поста
    async def send_post_now(self, update: Update, context: CallbackContext):
        if not self.current_post:
            await update.callback_query.message.reply_text("Нет активного поста для отправки.")
            return
        
        # Отправляем в канал
        if self.current_post['image_url']:
            await context.bot.send_photo(
                chat_id=config.CHANNEL_ID,
                photo=self.current_post['image_url'],
                caption=self.current_post['text']
            )
        else:
            await context.bot.send_message(
                chat_id=config.CHANNEL_ID,
                text=self.current_post['text']
            )
        self.current_post = None  # Сбрасываем пост
        await update.callback_query.message.reply_text("Пост отправлен в канал!")
        # Отправляем меню выбора действия
        keyboard = [
            [InlineKeyboardButton("День рождения знаменитости", callback_data='celebrity_birthday')],
            [InlineKeyboardButton("Фильм на вечер", callback_data='movie_night')],
            [InlineKeyboardButton("Новости из мира кино", callback_data='movie_news')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Какой пост вы хотите создать?",
            reply_markup=reply_markup
        )
post_manager = PostManager()