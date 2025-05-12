# 🤖 Celebrity Birthday Bot

Telegram-бот для автоматизированной публикации поздравлений с днём рождения знаменитостей.

## 📦 Стек технологий

- **Python**: 3.8  
- **python-telegram-bot**: 21.6 (поддерживает Telegram Bot API 8.3)  
- **python-dotenv**: 1.0.1  
- **requests**: 2.32.3 *(если используется)*  
- **SQLAlchemy**: 2.0.35 *(если используется)*  

## 💻 Среда разработки

- macOS, Bash/Zsh  
- Visual Studio Code (рекомендуется)  
- Все токены и ключи хранятся в `.env`, зависимости — в `requirements.txt`

## 📁 Структура проекта
celebrity_birthday_bot/
├── bot.py # Основной файл для запуска бота
├── config.py # Конфигурация (чтение из .env)
├── .env # Токены и конфиденциальные данные
├── requirements.txt # Список зависимостей

├── handlers/ # Обработчики команд и событий
│ ├── init.py
│ ├── user/ # Обработчики для пользователей
│ │ ├── init.py
│ │ ├── start.py # Обработчик /start и главное меню
│ │ ├── post_create.py # Создание постов (в т.ч. /celebrity_birthday)
│ │ └── echo.py # Обработка текстовых сообщений
│ └── admin/ # Административные команды (будущее)
│ ├── init.py
│ └── stats.py # Пример заглушки

├── modules/ # Бизнес-логика
│ ├── init.py
│ ├── post_manager.py # Управление логикой публикаций
│ └── celebrity_birthday.py # Логика постов с днями рождения

├── keyboards/ # Inline и reply-клавиатуры
│ ├── init.py
│ └── post_keyboard.py # Клавиатуры для управления постами

└── utils/ # Утилиты (в разработке)
└── init.py
