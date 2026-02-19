# main.py
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from config import API_TOKEN
from sources.registry import SOURCE_REGISTRY

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}


# ---------- Главное меню ----------
def main_menu_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Игры", "IT")
    kb.add("Наука", "Культура", "Бизнес")
    return kb


# ---------- /start ----------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Выберите категорию новостей:", reply_markup=main_menu_keyboard())


# ---------- Категории ----------
@dp.message_handler(lambda m: m.text in ["Игры", "IT", "Наука", "Культура", "Бизнес"])
async def choose_category(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    category = message.text
    # Получаем источники для категории из реестра
    sources = SOURCE_REGISTRY.get_sources_by_category(category)
    for src in sources:
        kb.add(src.name)
    kb.add("Назад в главное меню")
    await message.answer(f"Выберите источник для {category}:", reply_markup=kb)


# ---------- Назад ----------
@dp.message_handler(lambda m: m.text == "Назад в главное меню")
async def back(message: types.Message):
    await message.answer("Главное меню:", reply_markup=main_menu_keyboard())


# ---------- Показ новостей ----------
@dp.message_handler(lambda m: m.text in SOURCE_REGISTRY.get_all_source_names())
async def show_news(message: types.Message):
    source = SOURCE_REGISTRY.get_source_by_name(message.text)
    news_list = source.get_news()  # метод каждого источника

    if not news_list:
        await message.answer("Не удалось загрузить новости.")
        return

    user_data[message.from_user.id] = {"news": news_list, "index": 0}
    item = news_list[0]

    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Следующая новость", callback_data="next")
    )

    await message.answer(
        f"{item['title']}\n\n{item['summary']}\n{item['link']}",
        reply_markup=kb
    )


# ---------- Следующая новость ----------
@dp.callback_query_handler(lambda c: c.data == "next")
async def next_news(callback: types.CallbackQuery):
    data = user_data.get(callback.from_user.id)
    if not data:
        await callback.answer("Новости не найдены")
        return

    data["index"] += 1
    if data["index"] >= len(data["news"]):
        await callback.answer("Новости закончились")
        return

    item = data["news"][data["index"]]
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Следующая новость", callback_data="next")
    )

    await callback.message.edit_text(
        f"{item['title']}\n\n{item['summary']}\n{item['link']}",
        reply_markup=kb
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
