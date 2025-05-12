from telegram import Update
from telegram.ext import CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import config
from keyboards.post_keyboard import get_post_management_keyboard

class PostManager:
    def __init__(self):
        self.current_post = None
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    async def _send_management_buttons(self, context: CallbackContext, chat_id: int):
        reply_markup = get_post_management_keyboard()
        await context.bot.send_message(chat_id=chat_id, text="Управляйте постом:", reply_markup=reply_markup)

    async def send_post(self, update: Update, context: CallbackContext, text: str, image_url: str = None):
        chat_id = update.effective_chat.id
        if image_url:
            message = await context.bot.send_photo(chat_id=chat_id, photo=image_url, caption=text)
        else:
            message = await context.bot.send_message(chat_id=chat_id, text=text)
        self.current_post = {
            'chat_id': chat_id,
            'message_id': message.message_id,
            'text': text,
            'image_url': image_url
        }
        await self._send_management_buttons(context, chat_id)

    async def edit_post_text(self, update: Update, context: CallbackContext, new_text: str):
        if not self.current_post:
            await update.message.reply_text("Нет активного поста для редактирования.")
            return
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
        await self._send_management_buttons(context, self.current_post['chat_id'])

    async def edit_post_image(self, update: Update, context: CallbackContext, new_image_url: str):
        if not self.current_post:
            await update.message.reply_text("Нет активного поста для редактирования.")
            return
        self.current_post['image_url'] = new_image_url
        await context.bot.delete_message(
            chat_id=self.current_post['chat_id'],
            message_id=self.current_post['message_id']
        )
        message = await context.bot.send_photo(
            chat_id=self.current_post['chat_id'],
            photo=new_image_url,
            caption=self.current_post['text']
        )
        self.current_post['message_id'] = message.message_id
        await update.message.reply_text("Изображение поста обновлено.")
        await self._send_management_buttons(context, self.current_post['chat_id'])

    async def schedule_post(self, update: Update, context: CallbackContext, hour: int, minute: int):
        if not self.current_post:
            await update.callback_query.message.reply_text("Нет активного поста для планирования.")
            return
        def job():
            context.bot.send_message(
                chat_id=config.CHANNEL_ID,
                text=self.current_post['text']
            ) if not self.current_post['image_url'] else context.bot.send_photo(
                chat_id=config.CHANNEL_ID,
                photo=self.current_post['image_url'],
                caption=self.current_post['text']
            )
            self.current_post = None
        self.scheduler.add_job(job, 'cron', hour=hour, minute=minute)
        await update.callback_query.message.reply_text(f"Пост запланирован на {hour:02d}:{minute:02d}.")
        await self._send_management_buttons(context, self.current_post['chat_id'])

    async def reset_post(self, update: Update, context: CallbackContext):
        if not self.current_post:
            await update.callback_query.message.reply_text("Нет активного поста для сброса.")
            return
        self.current_post = None
        await update.callback_query.message.reply_text("Пост сброшён.")
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

    async def send_post_now(self, update: Update, context: CallbackContext):
        if not self.current_post:
            await update.callback_query.message.reply_text("Нет активного поста для отправки.")
            return
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
        self.current_post = None
        await update.callback_query.message.reply_text("Пост отправлен в канал!")
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