"""Модуль для обработки - /echo."""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command('echo'))
async def start(message: Message):
    """Обрабатывает команду /echo."""
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer('Хорошая попытка!')
