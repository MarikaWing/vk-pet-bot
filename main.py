import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Конфигурация
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_DOMAIN = os.getenv("WEBHOOK_DOMAIN")  # например: https://yourapp.onrender.com
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")
WEBHOOK_URL = f"{WEBHOOK_DOMAIN}{WEBHOOK_PATH}"
PORT = int(os.getenv("PORT", 10000))

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик сообщений
@dp.message(F.text)
async def echo(message: Message):
    await message.answer(f"Вы сказали: {message.text}")

# Функция для создания приложения aiohttp
def create_app():
    app = web.Application()

    # Отдаём HTML-файл по корневому маршруту /
    app.router.add_get("/", lambda request: web.FileResponse("static/index.html"))

    # Обработка Webhook запросов от Telegram
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)

    # Подключаем aiogram к приложению aiohttp
    setup_application(app, dp)

    # Устанавливаем Webhook при старте
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app

# Устанавливаем Webhook при старте
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    print(f"✅ Webhook установлен: {WEBHOOK_URL}")

# Очищаем Webhook при остановке
async def on_shutdown(app):
    await bot.delete_webhook()
    print("🛑 Webhook удалён")

# Точка входа
if __name__ == "__main__":
    web.run_app(create_app(), port=PORT)
