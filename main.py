import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Логирование (чтобы видеть ошибки)
logging.basicConfig(level=logging.INFO)

# Токены
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openchat/openchat-3.5"

# Основная функция для обработки сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Ты — Наташа, разговорчивая и остроумная."},
            {"role": "user", "content": user_message}
        ]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        bot_reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error(f"Ошибка при запросе к OpenRouter: {e}")
        bot_reply = "Упс! Я зависла, попробуй снова позже."

    await update.message.reply_text(bot_reply)

# Запуск бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
