from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, MessageHandler, Filters
import os

# Flask приложение
app = Flask(__name__)

# Telegram Bot токен
TOKEN = "8137862914:AAFhFzvF1m1ThXjz0N7R_5BhglJuGsdnhFI"
bot = Bot(token=TOKEN)

# Инициализация Dispatcher
dispatcher = Dispatcher(bot=bot, update_queue=None, use_context=True)

# Обработчик текстовых сообщений
def handle_message(update: Update, context):
    user_message = update.message.text
    chat_id = update.message.chat_id

    # Пример ответа
    context.bot.send_message(chat_id=chat_id, text=f"Вы сказали: {user_message}")

# Добавляем обработчик сообщений
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Вебхук для Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    # Получаем обновление от Telegram
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "Бот работает! Установите вебхук для взаимодействия.", 200

# Запуск приложения
if __name__ == "__main__":
    # Укажите ваш HTTPS URL для вебхука
    WEBHOOK_URL = "https://giftbot-xeca.vercel.app"
    bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
