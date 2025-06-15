import os, logging, requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)
TELEGRAM_TOKEN = os.getenv("7748771202:AAEVPCbnYwopGTtUbUeI_CDggNUHhS67ypg")
OPENROUTER_API_KEY = os.getenv("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")
MODEL = "openchat/openchat-3.5"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}
    payload = {"model": MODEL, "messages":[
        {"role":"system","content":"Ты — Наташа, разговорчивая и остроумная."},
        {"role":"user","content":text}
    ]}
    resp = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
    if resp.status_code == 200:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp.json()["choices"][0]["message"]["content"])
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="И снова глюк, попробуй позже.")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
