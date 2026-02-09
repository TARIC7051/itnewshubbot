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
    get_pitchfork_news, get_thequietus_news, get_aeon_news,
    get_nautilus_news
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
    kb.add(KeyboardButton("Кино"))
    kb.add(KeyboardButton("Музыка"))
    return kb

# --- Кнопка "назад в главное меню" ---
def back_to_main_keyboard():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Назад в главное меню"))
    return kb

# --- /start ---
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Выберите категорию новостей:",
                         reply_markup=main_menu_keyboard())

# --- Выбор категории ---
@dp.message_handler(
    lambda message: message.text in ["Игры", "IT", "Наука", "Технологии",
                                     "Культура", "Кино", "Музыка"])
async def category_chosen(message: types.Message):
    category = message.text
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    if category == "Игры":
        kb.add(KeyboardButton("StopGame"))
        kb.add(KeyboardButton("Igromania"))
        kb.add(KeyboardButton("Shazoo"))
        kb.add(KeyboardButton("Playground"))
        kb.add(KeyboardButton("3DNews"))
        kb.add(KeyboardButton("DTF"))
    elif category == "IT":
        kb.add(KeyboardButton("Habr"))
        kb.add(KeyboardButton("TechCrunch"))
        kb.add(KeyboardButton("The Verge"))
        kb.add(KeyboardButton("Slashdot"))
        kb.add(KeyboardButton("3DNews"))
    elif category == "Наука":
        kb.add(KeyboardButton("HackerNews"))
        kb.add(KeyboardButton("Aeon"))
        kb.add(KeyboardButton("Nautilus"))
    elif category == "Технологии":
        kb.add(KeyboardButton("TechCrunch"))
        kb.add(KeyboardButton("Slashdot"))
        kb.add(KeyboardButton("The Verge"))
        kb.add(KeyboardButton("3DNews"))
    elif category == "Культура":
        kb.add(KeyboardButton("PravilaMag"))
        kb.add(KeyboardButton("The Quietus"))
        kb.add(KeyboardButton("Pitchfork"))
    elif category == "Кино":
        kb.add(KeyboardButton("KinoPoisk"))
        kb.add(KeyboardButton("NoFilmSchool"))
    elif category == "Музыка":
        kb.add(KeyboardButton("Pitchfork"))
        kb.add(KeyboardButton("The Quietus"))

    kb.add(KeyboardButton("Назад в главное меню"))
    await message.answer(f"Вы выбрали {category}. Теперь выберите источник:",
                         reply_markup=kb)

# --- Назад в главное меню ---
@dp.message_handler(lambda message: message.text == "Назад в главное меню")
async def back_to_main(message: types.Message):
    await message.answer(
        "Вы вернулись в главное меню. Выберите категорию новостей:",
        reply_markup=main_menu_keyboard())

# --- Выбор источника ---
@dp.message_handler(lambda message: message.text in [
    "StopGame", "Igromania", "3DNews", "Habr", "TechCrunch",
    "The Verge", "HackerNews", "Slashdot", "Shazoo", "Playground",
    "PravilaMag", "KinoPoisk", "DTF", "NoFilmSchool", "Pitchfork",
    "The Quietus", "Aeon", "Nautilus"
])
async def source_chosen(message: types.Message):
    source = message.text

    # Получаем новости по источнику
    news_list = []
    if source == "StopGame":
        news_list = get_stopgame_news()
    elif source == "Igromania":
        news_list = get_igromania_news()
    elif source == "3DNews":
        news_list = get_3dnews_news()
    elif source == "Habr":
        news_list = get_habr_news()
    elif source == "TechCrunch":
        news_list = get_techcrunch_news()
    elif source == "The Verge":
        news_list = get_theverge_news()
    elif source == "HackerNews":
        news_list = get_hackernews()
    elif source == "Slashdot":
        news_list = get_slashdot_news()
    elif source == "Shazoo":
        news_list = get_shazoo_news()
    elif source == "Playground":
        news_list = get_playground_news()
    elif source == "PravilaMag":
        news_list = get_pravilamag_news()
    elif source == "KinoPoisk":
        news_list = get_kinopoisk_news()
    elif source == "DTF":
        news_list = get_dtf_news()
    elif source == "NoFilmSchool":
        news_list = get_nofilmschool_news()
    elif source == "Pitchfork":
        news_list = get_pitchfork_news()
    elif source == "The Quietus":
        news_list = get_thequietus_news()
    elif source == "Aeon":
        news_list = get_aeon_news()
    elif source == "Nautilus":
        news_list = get_nautilus_news()

    if not news_list:
        await message.answer("Не удалось получить новости.")
        return

    user_data[message.from_user.id] = {"news": news_list, "index": 0}

    news_item = news_list[0]
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Следующая новость",
                                callback_data="next_news"))

    text = f"{news_item['title']}\n\n{news_item['summary']}\n{news_item['link']}"
    await message.answer(text, reply_markup=kb)

# --- Callback для следующей новости ---
@dp.callback_query_handler(lambda c: c.data == "next_news")
async def next_news(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    data = user_data.get(user_id)
    if not data:
        await callback_query.answer(
            "Новости не найдены. Сначала выберите источник.")
        return

    data['index'] += 1
    if data['index'] >= len(data['news']):
        await callback_query.answer("Больше новостей нет.")
        return

    news_item = data['news'][data['index']]
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("Следующая новость",
                                callback_data="next_news"))

    text = f"{news_item['title']}\n\n{news_item['summary']}\n{news_item['link']}"
    await callback_query.message.edit_text(text, reply_markup=kb)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
