import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from config import API_TOKEN
from news import (
    get_3dnews_news, get_habr_news, get_hackernews,
    get_theverge_news, get_techcrunch_news, get_slashdot_news,
    get_stopgame_news, get_igromania_news,
    get_shazoo_news, get_playground_news, get_pravilamag_news,
    get_kinopoisk_news, get_dtf_news, get_nofilmschool_news,
    get_pitchfork_news, get_thequietus_news, get_aeon_news, get_nautilus_news
)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}  # новости и индекс для каждого пользователя

# --- Кнопки главного меню ---
def main_menu_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Игры"))
    kb.add(KeyboardButton("IT"))
    kb.add(KeyboardButton("Наука"))
    kb.add(KeyboardButton("Технологии"))
    kb.add(KeyboardButton("Культура"))
    return kb


# --- Кнопка "назад в главное меню" ---
def back_to_main_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Назад в главное меню"))
    return kb


# --- /start ---
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Выберите категорию новостей:", reply_markup=main_menu_keyboard())


# --- Выбор категории ---
@dp.message_handler(lambda message: message.text in ["Игры", "IT", "Наука", "Технологии", "Культура"])
async def category_chosen(message: types.Message):
    category = message.text
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    if category == "Игры":
        kb.add(KeyboardButton("StopGame"))
        kb.add(KeyboardButton("Igromania"))
        kb.add(KeyboardButton("Shazoo"))
        kb.add(KeyboardButton("Playground"))
    elif category == "IT":
        kb.add(KeyboardButton("3DNews"))
        kb.add(KeyboardButton("Habr"))
        kb.add(KeyboardButton("TechCrunch"))
        kb.add(KeyboardButton("The Verge"))
        kb.add(KeyboardButton("Slashdot"))
        kb.add(KeyboardButton("DTF"))
    elif category == "Наука":
        kb.add(KeyboardButton("HackerNews"))
        kb.add(KeyboardButton("Aeon"))
        kb.add(KeyboardButton("Nautilus"))
    elif category == "Технологии":
        kb.add(KeyboardButton("TechCrunch"))
        kb.add(KeyboardButton("The Verge"))
        kb.add(KeyboardButton("Slashdot"))
        kb.add(KeyboardButton("NoFilmSchool"))
    elif category == "Культура":
        kb.add(KeyboardButton("Pitchfork"))
        kb.add(KeyboardButton("The Quietus"))
        kb.add(KeyboardButton("PravilaMag"))
        kb.add(KeyboardButton("KinoPoisk"))

    kb.add(KeyboardButton("Назад в главное меню"))
    await message.answer(f"Вы выбрали {category}. Теперь выберите источник:", reply_markup=kb)


# --- Назад в главное меню ---
@dp.message_handler(lambda message: message.text == "Назад в главное меню")
async def back_to_main(message: types.Message):
    await message.answer("Вы вернулись в главное меню. Выберите категорию новостей:", reply_markup=main_menu_keyboard())


# --- Словарь источников ---
source_functions = {
    "StopGame": get_stopgame_news,
    "Igromania": get_igromania_news,
    "3DNews": get_3dnews_news,
    "Habr": get_habr_news,
    "TechCrunch": get_techcrunch_news,
    "The Verge": get_theverge_news,
    "HackerNews": get_hackernews,
    "Slashdot": get_slashdot_news,
    "Shazoo": get_shazoo_news,
    "Playground": get_playground_news,
    "PravilaMag": get_pravilamag_news,
    "KinoPoisk": get_kinopoisk_news,
    "DTF": get_dtf_news,
    "NoFilmSchool": get_nofilmschool_news,
    "Pitchfork": get_pitchfork_news,
    "The Quietus": get_thequietus_news,
    "Aeon": get_aeon_news,
    "Nautilus": get_nautilus_news
}


# --- Выбор источника ---
@dp.message_handler(lambda message: message.text in source_functions.keys())
async def source_chosen(message: types.Message):
    source = message.text
    news_list = source_functions[source]()
    if not news_list:
        await message.answer("Не удалось получить новости.")
        return

    user_data[message.from_user.id] = {"news": news_list, "index": 0}

    news_item = news_list[0]
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Следующая новость", callback_data="next_news"))

    text = f"{news_item['title']}\n\n{news_item['summary']}\n{news_item['link']}"
    await message.answer(text, reply_markup=kb)


# --- Callback для следующей новости ---
@dp.callback_query_handler(lambda c: c.data == "next_news")
async def next_news(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = user_data.get(user_id)
    if not data:
        await callback_query.answer("Новости не найдены. Сначала выберите источник.")
        return

    data['index'] += 1
    if data['index'] >= len(data['news']):
        await callback_query.answer("Больше новостей нет.")
        return

    news_item = data['news'][data['index']]
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Следующая новость", callback_data="next_news"))

    text = f"{news_item['title']}\n\n{news_item['summary']}\n{news_item['link']}"
    await callback_query.message.edit_text(text, reply_markup=kb)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
