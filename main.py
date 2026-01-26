# main.py

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH

# логирование
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(
        "ITNewsHubBot запущен.\n"
        "Скоро здесь будут новости IT-индустрии."
    )


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info(f"Webhook set to {WEBHOOK_URL}")


async def on_shutdown(dispatcher):
    await bot.delete_webhook()
    logging.info("Webhook deleted")


if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host="0.0.0.0",
        port=8000
    )
