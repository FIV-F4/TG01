import asyncio
from aiogram import Bot, Router, Dispatcher, F
from aiogram.types import Message, FSInputFile, CallbackQuery, KeyboardButton
from aiogram.filters import CommandStart, Command
import random
import keyboards as kb
import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import requests

from config import TOKEN
import sqlite3
import logging


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
router = Router()
storage = MemoryStorage()

button_registr = KeyboardButton(text="Регистрация в телеграм боте")
button_exchange_rates = KeyboardButton(text="Курс валют")
button_tips = KeyboardButton(text="Советы по экономии")
button_finance = KeyboardButton(text="Личные финансы")

keyboards = ReplyKeyboardMarkup(keyboard=[
    [button_registr, button_exchange_rates],
    [button_tips, button_finance]
], resize_keyboard=True)


conn = sqlite3.connect('user.db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY AUTOINCREMENT, 
               telegram_id INTEGER NOT NULL UNIQUE,
               name TEXT NOT NULL, 
               category1 TEXT,
               category2 TEXT,
               category3 TEXT,
               expenses1 REAL,
               expenses2 REAL,
               expenses3 REAL)''')

conn.commit()

class FinancesForm(StatesGroup):
    category1 = State()
    category2 = State()
    category3 = State()
    expenses1 = State()
    expenses2 = State()
    expenses3 = State()

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer("Привет, я бот для учёта доходов и расходов. Чем я могу помочь?", reply_markup=keyboards)
@router.message(F.text == "Регистрация в телеграм боте")
async def registr(message: Message):
    telegram_id = message.from_user.id
    name = message.from_user.full_name
    cur.execute('''SELECT * FROM users WHERE telegram_id = ?''', (telegram_id,))
    user = cur.fetchone()

    if user is None:
        cur.execute('''INSERT INTO users (telegram_id, name) VALUES (?, ?)''', (telegram_id, name))
        conn.commit()
        await message.answer("Вы зарегистрированы в боте. Спасибо за регистрацию")
    else:
        await message.answer("Вы уже зарегистрированы в боте")

@router.message(F.text == "Курс валют")
async def exchange_rates(message: Message):
    url = "https://v6.exchangerate-api.com/v6/df900b116f5776e7d8ca3e4c/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            await message.answer("Произошла ошибка (Ответ не 200)")
            return
        usd_to_rub = data["conversion_rates"]["RUB"]
        eur_to_usd = data["conversion_rates"]["EUR"]

        eur_to_rub = eur_to_usd * usd_to_rub
        await message.answer(f"1 EUR = {eur_to_rub:.2f} RUB\n1 USD = {usd_to_rub:.2f} RUB")

    except:
        await message.answer("Произошла ошибка")

@router.message(F.text == "Советы по экономии")
async def tips(message: Message):
    await message.answer("Здесь могла быть ваша реклама")


@router.message(F.text == "Личные финансы")
async def finance(message: Message, state: FSMContext):
    await state.set_state(FinancesForm.category1)
    await message.answer("Введите категорию расходов")

@router.message(FinancesForm.category1)
async def finance(message: Message, state: FSMContext):
    await state.update_data(category1=message.text)
    await state.set_state(FinancesForm.expenses1)
    await message.answer("Введите расходы для категории1")

@router.message(FinancesForm.expenses1)
async def finance(message: Message, state: FSMContext):
    await state.update_data(expenses1=float(message.text))
    await state.set_state(FinancesForm.category2)
    await message.answer("Введите категорию расходов 2")

@router.message(FinancesForm.category2)
async def finance(message: Message, state: FSMContext):
    await state.update_data(category2=message.text)
    await state.set_state(FinancesForm.expenses2)
    await message.answer("Введите расходы для категории2")

@router.message(FinancesForm.expenses2)
async def finance(message: Message, state: FSMContext):
    await state.update_data(expenses2=float(message.text))
    await state.set_state(FinancesForm.category3)
    await message.answer("Введите категорию расходов 3")

@router.message(FinancesForm.category3)
async def finance(message: Message, state: FSMContext):
    await state.update_data(category3=message.text)
    await state.set_state(FinancesForm.expenses3)
    await message.answer("Введите расходы для категории3")

@router.message(FinancesForm.expenses3)
async def finance(message: Message, state: FSMContext):
    await state.update_data(expenses3=float(message.text))
    data = await state.get_data()
    telegram_id = message.from_user.id
    cur.execute('''UPDATE users SET category1 = ?, category2 = ?, category3 = ?, expenses1 = ?, expenses2 = ?, expenses3 = ? WHERE telegram_id = ?''',
                (data['category1'], data['category2'], data['category3'], data['expenses1'], data['expenses2'], data['expenses3'], telegram_id))
    conn.commit()
    await state.clear()
    await message.answer("Категории и расходы сохранены")

async def main():
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())