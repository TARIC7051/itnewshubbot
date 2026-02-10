import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.utils import executor
from config import API_TOKEN
from news import (
    get_3dnews_news,
    get_habr_news,
    get_hackernews,
    get_theverge_news,
    get_techcrunch_news,
    get_slashdot_news,
    get_stopgame_news,
    get_igromania_news,
    get_shazoo_news,
    get_playground_news,      # ← ВАЖНО
    get_pravilamag_news,
    get_kinopoisk_news,
    get_dtf_news,
    get_nofilmschool_news,
    get_pitchfork_news,
    get_thequietus_news,
    get_aeon_news,
    get_nautilus_news
)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}


# ---------- Главное меню ----------
def main_menu_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Игры", "IT")
    kb.add("Наука", "Культура")
    return kb


# ---------- /start ----------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "Выберите категорию новостей:",
        reply_markup=main_menu_keyboard()
    )


# ---------- Категории ----------
@dp.message_handler(lambda m: m.text in ["Игры", "IT", "Наука", "Культура"])
async def choose_category(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    if message.text == "Игры":
        kb.add("StopGame", "Igromania", "Shazoo", "Playground", "DTF")
    elif message.text == "IT":
        kb.add("3DNews", "Habr", "TechCrunch", "The Verge", "Slashdot")
    elif message.text == "Наука":
        kb.add("HackerNews", "Aeon", "Nautilus")
    elif message.text == "Культура":
        kb.add("Pitchfork", "The Quietus", "PravilaMag", "KinoPoisk", "NoFilmSchool")

    kb.add("Назад в главное меню")
    await message.answer("Выберите источник:", reply_markup=kb)


# ---------- Назад ----------
@dp.message_handler(lambda m: m.text == "Назад в главное меню")
async def back(message: types.Message):
    await message.answer(
        "Главное меню:",
        reply_markup=main_menu_keyboard()
    )


# ---------- Карта источников ----------
SOURCE_MAP = {
    "StopGame": get_stopgame_news,
    "Igromania": get_igromania_news,
    "Shazoo": get_shazoo_news,
    "Playground": get_playground_news,   # ← ВАЖНО
    "DTF": get_dtf_news,
    "3DNews": get_3dnews_news,
    "Habr": get_habr_news,
    "TechCrunch": get_techcrunch_news,
    "The Verge": get_theverge_news,
    "Slashdot": get_slashdot_news,
    "HackerNews": get_hackernews,
    "Aeon": get_aeon_news,
    "Nautilus": get_nautilus_news,
    "Pitchfork": get_pitchfork_news,
    "The Quietus": get_thequietus_news,
    "PravilaMag": get_pravilamag_news,
    "KinoPoisk": get_kinopoisk_news,
    "NoFilmSchool": get_nofilmschool_news,
}


# ---------- Выбор источника ----------
@dp.message_handler(lambda m: m.text in SOURCE_MAP)
async def show_news(message: types.Message):
    news_list = SOURCE_MAP[message.text]()

    if not news_list:
        await message.answer("Не удалось загрузить новости.")
        return

    user_data[message.from_user.id] = {
        "news": news_list,
        "index": 0
    }

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
async def next_news(cb: types.CallbackQuery):
    data = user_data.get(cb.from_user.id)
    if not data:
        await cb.answer("Новости не найдены")
        return

    data["index"] += 1
    if data["index"] >= len(data["news"]):
        await cb.answer("Новости закончились")
        return

    item = data["news"][data["index"]]
    kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Следующая новость", callback_data="next")
    )

    await cb.message.edit_text(
        f"{item['title']}\n\n{item['summary']}\n{item['link']}",
        reply_markup=kb
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
