# Импортируем необходимые модули
import logging  # Для логирования работы бота
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters  # type: ignore # Классы для обработки сообщений и команд
import config  # Импортируем настройки из config.py
import handlers  # Импортируем обработчики из handlers.py

# Настраиваем логирование для отладки
# Логи будут показывать время, имя модуля, уровень и сообщение
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Асинхронная функция для настройки после инициализации
async def post_init(application):
    await handlers.setup_commands(application.bot)

# Основная функция для запуска бота
def main():
    # Инициализируем приложение с токеном из config.py
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).post_init(post_init).build()

    # Добавляем обработчики команд из handlers.py
    application.add_handler(CommandHandler("start", handlers.start))
    application.add_handler(CommandHandler("celebrity_birthday", handlers.celebrity_birthday))
    application.add_handler(CommandHandler("movie_night", handlers.movie_night))
    application.add_handler(CommandHandler("movie_news", handlers.movie_news))
    application.add_handler(CommandHandler("edit_text", handlers.edit_text))
    application.add_handler(CommandHandler("edit_image", handlers.edit_image))
    application.add_handler(CommandHandler("schedule", handlers.schedule))
    application.add_handler(CommandHandler("reset", handlers.reset))
    application.add_handler(CommandHandler("send_now", handlers.send_now))

    # Добавляем обработчик для нажатий на кнопки
    application.add_handler(CallbackQueryHandler(handlers.button_callback))

    # Добавляем обработчик для всех текстовых сообщений, кроме команд
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.echo))

    # Добавляем обработчик для загруженных фотографий
    application.add_handler(MessageHandler(filters.PHOTO, handlers.handle_photo))

    # Запускаем бота в режиме polling (опроса серверов Telegram)
    application.run_polling()

# Проверяем, что скрипт запущен напрямую, а не импортирован
if __name__ == '__main__':
    main()