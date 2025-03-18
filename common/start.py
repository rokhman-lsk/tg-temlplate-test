"""Модуль для обработки - /start."""
from aiogram import Router, html
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command('start'))
async def start(message: Message):
    """Обрабатывает команду /start."""
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    await message.answer("""
----------------------------------------
🏢 Основная логика
----------------------------------------
/command - делает что-то полезное

/echo - и так понятно
----------------------------------------
✍️ Обратная связь
----------------------------------------
/feedback - отправить
----------------------------------------
🔧 Админ
----------------------------------------
/admin - админ панель
----------------------------------------
🌐 Наш сайт - https://
----------------------------------------
""")
