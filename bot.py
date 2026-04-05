import asyncio
import logging
import sqlite3
import os

from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.filters import Command

TOKEN = os.getenv("8675971570:AAG-j39zbGTACNWOH858w7v-okAbvNNri3E")

# ---------------- LOGGING ----------------

logging.basicConfig(level=logging.INFO)

# ---------------- DATABASE ----------------

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
username TEXT
)
""")

conn.commit()


def add_user(user_id, username):
    cursor.execute(
        "INSERT INTO users(user_id, username) VALUES (?, ?)",
        (user_id, username)
    )
    conn.commit()


# ---------------- BOT INIT ----------------

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ---------------- KEYBOARDS ----------------

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💄 Підібрати косметику")],
        [KeyboardButton(text="ℹ️ Інформація")]
    ],
    resize_keyboard=True
)

skin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Суха", callback_data="dry")],
        [InlineKeyboardButton(text="Жирна", callback_data="oily")],
        [InlineKeyboardButton(text="Комбінована", callback_data="combo")],
        [InlineKeyboardButton(text="Чутлива", callback_data="sensitive")]
    ]
)

problem_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Акне", callback_data="acne")],
        [InlineKeyboardButton(text="Сухість", callback_data="dry_skin")],
        [InlineKeyboardButton(text="Зморшки", callback_data="wrinkles")],
        [InlineKeyboardButton(text="Пігментація", callback_data="pigment")]
    ]
)

# ---------------- COMMANDS ----------------

@dp.message(Command("start"))
async def start_command(message: Message):

    add_user(message.from_user.id, message.from_user.username)

    await message.answer(
        "👋 Вітаю!\n"
        "Я бот для індивідуального підбору косметики.",
        reply_markup=main_keyboard
    )


@dp.message(Command("help"))
async def help_command(message: Message):

    await message.answer(
        "/start — запуск бота\n"
        "/help — допомога\n"
        "/info — інформація"
    )


@dp.message(Command("info"))
async def info_command(message: Message):

    await message.answer(
        "Цей бот допомагає підібрати косметику "
        "відповідно до типу шкіри та проблем."
    )

# ---------------- PHOTO HANDLER ----------------

@dp.message(F.photo)
async def photo_handler(message: Message):

    await message.answer(
        "📷 Фото отримано.\n"
        "У майбутньому бот може аналізувати стан шкіри."
    )

# ---------------- TEXT HANDLER ----------------

@dp.message()
async def text_handler(message: Message):

    if message.text == "💄 Підібрати косметику":

        await message.answer(
            "Оберіть тип шкіри:",
            reply_markup=skin_keyboard
        )

    elif message.text == "ℹ️ Інформація":

        await message.answer(
            "Бот підбирає косметику на основі:\n"
            "• типу шкіри\n"
            "• проблем шкіри"
        )

    else:

        await message.answer("Я не зрозумів повідомлення.")

# ---------------- CALLBACKS ----------------

@dp.callback_query(F.data == "dry")
async def dry_skin(callback: CallbackQuery):

    await callback.message.answer(
        "Оберіть проблему шкіри:",
        reply_markup=problem_keyboard
    )


@dp.callback_query(F.data == "oily")
async def oily_skin(callback: CallbackQuery):

    await callback.message.answer(
        "Оберіть проблему шкіри:",
        reply_markup=problem_keyboard
    )


@dp.callback_query(F.data == "combo")
async def combo_skin(callback: CallbackQuery):

    await callback.message.answer(
        "Оберіть проблему шкіри:",
        reply_markup=problem_keyboard
    )


@dp.callback_query(F.data == "sensitive")
async def sensitive_skin(callback: CallbackQuery):

    await callback.message.answer(
        "Оберіть проблему шкіри:",
        reply_markup=problem_keyboard
    )

# ---------------- PROBLEMS ----------------

@dp.callback_query(F.data == "acne")
async def acne_problem(callback: CallbackQuery):

    await callback.message.answer(
        "Рекомендації при акне:\n"
        "• гель з саліциловою кислотою\n"
        "• крем з ніацинамідом\n"
        "• легкий зволожуючий крем"
    )


@dp.callback_query(F.data == "dry_skin")
async def dry_problem(callback: CallbackQuery):

    await callback.message.answer(
        "Рекомендації при сухості:\n"
        "• крем з гіалуроновою кислотою\n"
        "• живильна сироватка\n"
        "• м’який очищуючий засіб"
    )


@dp.callback_query(F.data == "wrinkles")
async def wrinkles_problem(callback: CallbackQuery):

    await callback.message.answer(
        "Антивіковий догляд:\n"
        "• ретинол\n"
        "• пептиди\n"
        "• крем з SPF"
    )


@dp.callback_query(F.data == "pigment")
async def pigment_problem(callback: CallbackQuery):

    await callback.message.answer(
        "Рекомендації при пігментації:\n"
        "• вітамін C\n"
        "• освітлююча сироватка\n"
        "• крем з SPF"
    )

# ---------------- MAIN ----------------

async def main():

    try:
        await dp.start_polling(bot)

    except Exception as e:
        logging.error(f"Помилка роботи бота: {e}")


if __name__ == "__main__":
    asyncio.run(main())
