import os
import openai
import telebot
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Инициализация
bot = telebot.TeleBot(TELEGRAM_TOKEN)
openai.api_key = OPENAI_API_KEY

# Стартовое сообщение
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Введи параметры авто: \n\n• Марка\n• Год выпуска\n• Объем двигателя\n• Цена в юанях\n• Дата ввоза в РФ\n\nПример: Honda Civic 2021, 1.5 л, 89800 юаней, ввоз в апреле 2025"
    )

# Обработка сообщений
@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_input = message.text

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты помощник, который рассчитывает стоимость автомобиля из Китая для клиента в РФ, включая все таможенные расходы, доставку, брокера, конвертацию юаней и т.д."},
                {"role": "user", "content": user_input}
            ]
        )
        answer = response.choices[0].message.content.strip()
        bot.send_message(message.chat.id, answer)

    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обработке: {str(e)}")

# Запуск
bot.polling()
