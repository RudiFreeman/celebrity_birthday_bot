проект собран на
Python: 3.8.
python-telegram-bot: 21.6 (поддерживает Telegram Bot API 8.3).
python-dotenv: 1.0.1.
requests (если используется): 2.32.3.
SQLAlchemy (если используется): 2.0.35.
Среда: macOS, Bash/Zsh, вероятно Visual Studio Code.
Конфигурация: Токены в .env, зависимости в requirements.txt.




Структура 

telegram_bot/
├── bot.py                       # Основной файл для запуска бота
├── config.py                    # Конфигурация (чтение из .env)
├── .env                         # Токены и конфиденциальные данные
├── requirements.txt             # Список зависимостей
├── handlers/                    # Обработчики команд и событий
│   ├── __init__.py
│   ├── user/                   # Обработчики для пользователей
│   │   ├── __init__.py
│   │   ├── start.py            # Обработчик /start и меню
│   │   ├── post_create.py      # Создание постов (/celebrity_birthday и др.)
│   │   └── echo.py             # Обработка текстовых сообщений
│   └── admin/                  # Будущие административные команды
│       ├── __init__.py
│       └── stats.py            # Пример (пока пустой)
├── modules/                    # Бизнес-логика
│   ├── __init__.py
│   ├── post_manager.py         # Управление постами
│   └── celebrity_birthday.py   # Логика постов о днях рождения
├── keyboards/                  # Клавиатуры
│   ├── __init__.py
│   └── post_keyboard.py        # Клавиатуры для управления постами
└── utils/                      # Утилиты (пока пусто)
    └── __init__.py# celebrity_birthday_bot
