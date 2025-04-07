import os
import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

openai.api_key = os.getenv("OPENAI_API_KEY")

async def get_gpt_response(user_input: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты помощник, который рассчитывает полную стоимость автомобиля при ввозе из Китая в Россию. Учитывай курс юаня, категорию (до 3 лет / 3-5 лет / старше), объем двигателя и прочие стандартные пошлины."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message["content"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Введи параметры авто: марка, год, объем двигателя, цена в юанях, дата ввоза в РФ.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    reply = await get_gpt_response(user_input)
    await update.message.reply_text(reply)

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
