from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def handle_all(message: Message):
    await message.answer(f"📝 Вы написали: {message.text}")
