import logging

from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config import BOT_TOKEN
from news import get_all_news

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(
        "ITNewsHubBot запущен.\n"
        "Команда /news — последние IT-новости."
    )


@dp.message_handler(commands=["news"])
async def cmd_news(message: types.Message):
    news_list = get_all_news(limit=5)

    if not news_list:
        await message.answer("Не удалось получить новости.")
        return

    for item in news_list:
        await message.answer(item)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
