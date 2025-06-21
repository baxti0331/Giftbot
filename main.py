from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
import asyncio
import os

# 🔐 Настройки — замени на свои
BOT_TOKEN = "your_bot_token_here"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://yourdomain.com{WEBHOOK_PATH}"  # <--- замени!

# 🎛️ Инициализация
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()
app = FastAPI()

# 📩 Обработка сообщений
@dp.message()
async def handle_message(message: types.Message):
    await message.answer(f"👋 Привет! Ты сказал: {message.text}")

# 🚀 При запуске приложения
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook установлен на {WEBHOOK_URL}")

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await bot.session.close()
    print("🛑 Webhook удалён и бот остановлен")

# 📬 Обработка обновлений от Telegram
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}
