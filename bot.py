import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiohttp import web

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например, https://yourapp.onrender.com/webhook

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("🐾 Привет! Я бот для поиска животных в Ижевске.")

@dp.message(commands=["status"])
async def status_cmd(message: types.Message):
    await message.answer("✅ Всё работает!")

@dp.message(commands=["test"])
async def test_cmd(message: types.Message):
    await message.answer("🧪 Тест пройден!")

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

async def handle(request):
    data = await request.json()
    update = types.Update(**data)
    await dp.process_update(update)
    return web.Response(text="OK")

app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle)

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    web.run_app(app, host="0.0.0.0", port=port)
