from datetime import datetime
from modules.post_manager import post_manager

async def create_birthday_post(update, context):
    months = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
        7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
    }
    current_date = datetime.now()
    formatted_date = f"{current_date.day} {months[current_date.month]} {current_date.year}"
    celebrity_name = "[Знаменитость]"
    age = "[x]"
    movies = [
        ("Титаник", 1997),
        ("Волк с Уолл-стрит", 2013),
        ("Начало", 2010)
    ]
    post_text = f"Сегодня {formatted_date} родился {celebrity_name}, ему исполнилось {age} лет\n"
    post_text += "Его лучшие фильмы:\n"
    post_text += "\n".join(f"- {movie} ({year})" for movie, year in movies)
    post_text += "\nКакой тебе больше всего понравился?"
    await post_manager.send_post(update, context, post_text, image_url=None)