from fastapi import FastAPI, Request
from aiogram.types import Update

from bot import bot, dp
from config import settings
from handlers import router as main_router

app = FastAPI()

# Регистрация хендлеров
dp.include_router(main_router)


@app.on_event("startup")
async def startup():
    await bot.set_webhook(settings.webhook_url)
    print("✅ Webhook установлен:", settings.webhook_url)


@app.on_event("shutdown")
async def shutdown():
    await bot.delete_webhook()
    await bot.session.close()
    print("🛑 Webhook удалён и бот выключен")


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}
