from fastapi import Request
from aiogram.types import Update
from fastapi.responses import JSONResponse

from bot import bot, dp
from config import WEBHOOK_URL
from handlers import router

dp.include_router(router)

async def webhook(request: Request):
    update_dict = await request.json()
    update = Update(**update_dict)
    await dp.feed_update(bot, update)
    return JSONResponse({"ok": True})
