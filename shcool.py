import asyncio
import aiohttp
from aiogram import Bot, Router, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, WEATHER_TOKEN
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
router = Router()
storage = MemoryStorage()

# Определяем состояния для машины состояний
class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                   (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, age INTEGER NOT NULL, grade TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# Обработка команды /start
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

@router.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

@router.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("В каком ты классе?")
    await state.set_state(Form.grade)

@router.message(Form.grade)
async def name(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, age, grade) VALUES (?, ?, ?)", (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()

    await message.answer("Запись успешно добавлена!")
    await state.clear()

# Запуск бота
async def main():
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
