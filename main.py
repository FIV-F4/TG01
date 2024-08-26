import asyncio
from aiogram import Bot, Router, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from config import TOKEN
import random

bot = Bot(token=TOKEN)
router = Router()

@router.message(Command('photo'))
async def photo(message: Message):
    list = ['https://cdn.fishki.net/upload/post/2021/02/16/3613183/2e037d6c10de68fc5fe87943b902b62d.jpg', 'https://www.youloveit.ru/uploads/gallery/main/162/pikachu.png', 'https://shapka-youtube.ru/wp-content/uploads/2022/11/ava-s-nadpisyu-abonent-nedostupen.jpg']
    rand_answ = random.choice(list)
    await message.answer_photo(photo=rand_answ, caption="Картинка")
@router.message(Command('help'))
async def help(message: Message):
    await message.answer(f"Тут будет помощь =)")

@router.message(Command('Weather'))
async def help(message: Message):
    await message.answer(f"Тут будет помощь =)")
@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Я бот =)")

@router.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer(f"Терминатор бу-ха-ха")

@router.message(F.photo)
async def photoText(message: Message):
    list = ['Ого какая фотка', 'Не понятно что это' , 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)




home.openweathermap.org

async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
