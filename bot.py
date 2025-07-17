import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("🐾 Привет! Я бот для поиска животных в Ижевске.")

@dp.message(Command("status"))
async def status_cmd(message: types.Message):
    await message.answer("✅ Всё работает!")

@dp.message(Command("test"))
async def test_cmd(message: types.Message):
    await message.answer("🧪 Тест пройден!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
