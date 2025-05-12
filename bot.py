import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import config
from handlers.user.start import start, setup_commands
from handlers.user.post_create import celebrity_birthday, movie_night, movie_news
from handlers.user.echo import echo
from handlers.user.post_actions import edit_text, edit_image, schedule, reset, send_now, button_callback, handle_photo

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def post_init(application):
    await setup_commands(application.bot)

def main():
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).post_init(post_init).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("celebrity_birthday", celebrity_birthday))
    application.add_handler(CommandHandler("movie_night", movie_night))
    application.add_handler(CommandHandler("movie_news", movie_news))
    application.add_handler(CommandHandler("edit_text", edit_text))
    application.add_handler(CommandHandler("edit_image", edit_image))
    application.add_handler(CommandHandler("schedule", schedule))
    application.add_handler(CommandHandler("reset", reset))
    application.add_handler(CommandHandler("send_now", send_now))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.run_polling()

if __name__ == '__main__':
    main()