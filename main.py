import asyncio
from aiogram import Bot, Router, Dispatcher, F
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.filters import CommandStart, Command
from config import TOKEN
import random
from gtts import gTTS
import os
from deep_translator import GoogleTranslator
from meteo import get_weather
import keyboards as kb





bot = Bot(token=TOKEN)
router = Router()
'''
@router.callback_query(F.data == "news")
async def news(callback: CallbackQuery):
    await callback.answer("Новости подгружаются", show_alert=True)
    await callback.message.answer("Вот свежие новости")
'''
@router.callback_query(F.data == "news")
async def news(callback: CallbackQuery):
    await callback.answer("Новости подгружаются", show_alert=True)
    await callback.message.edit_text("Вот свежие новости", reply_markup=await kb.test_keyboard())

@router.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('video.mp4')
    await bot.send_video(message.chat.id, video)

@router.message(Command('audio'))
async def audio(message: Message):
    audio = FSInputFile('audio.mp3')
    await bot.send_audio(message.chat.id, audio)

@router.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile('PDF.pdf')
    await bot.send_document(message.chat.id, doc)
@router.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile('voice.ogg')
    await bot.send_voice(message.chat.id, voice)


@router.message(Command('training'))
async def training(message: Message):
    training_list = [
    '1',
    '2',
    '3'
    ]
    rand_training = random.choice(training_list)
    await message.answer(f"Тренировка {rand_training} пройдена")

    tts = gTTS(text=f"Тренировка {rand_training} пройдена", lang='ru')
    tts.save('audioTraining.ogg')
    audio = FSInputFile('audioTraining.ogg')
    await bot.send_voice(message.chat.id, audio)
    os.remove('audioTraining.ogg')


@router.message(Command('photo',prefix='&'))
async def photo(message: Message):
    list = ['https://cdn.fishki.net/upload/post/2021/02/16/3613183/2e037d6c10de68fc5fe87943b902b62d.jpg', 'https://www.youloveit.ru/uploads/gallery/main/162/pikachu.png', 'https://shapka-youtube.ru/wp-content/uploads/2022/11/ava-s-nadpisyu-abonent-nedostupen.jpg']
    rand_answ = random.choice(list)
    await message.answer_photo(photo=rand_answ, caption="Картинка")
@router.message(Command('help'))
async def help(message: Message):
    await message.answer(f"Тут будет помощь =)")

@router.message(Command('dynamic'))
async def dynamic(message: Message):
    await message.answer("...", reply_markup=kb.inline_keyboard_test2)

@router.callback_query(F.data == "dynamic1")
async def news(callback: CallbackQuery):
    await callback.answer("Обновление кнопок", show_alert=True)
    await callback.message.edit_text("...", reply_markup=kb.inline_keyboard_test3)

@router.callback_query(F.data == "dynamic1_1")
async def news(callback: CallbackQuery):
    await callback.message.answer("Опция 1")

@router.callback_query(F.data == "dynamic1_2")
async def news(callback: CallbackQuery):
    await callback.message.answer("Опция 2")

@router.message(Command('links'))
async def links(message: Message):
    await message.answer(f"Полезные ссылки:", reply_markup=kb.inline_keyboard_test)
@router.message(Command('Weather'))
async def Weather(message: Message):
    latitude = 59.57  # СПБ
    longitude = 30.19  # СПБ
    answer = get_weather(latitude, longitude)
    await message.answer(answer)
@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}! Я бот =)", reply_markup=kb.main) #reply_markup=await kb.test_keyboard())

@router.message(F.text == "Привет")
async def hello(message: Message):
    await message.answer(f"Приветик, {message.from_user.full_name}!")

@router.message(F.text == "Пока")
async def goodbye(message: Message):
    await message.answer(f"Пока, {message.from_user.full_name}!")


@router.message(F.photo)
async def photoText(message: Message):
    list = ['Ого какая фотка', 'Не понятно что это' , 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')

@router.message()
async def message(message: Message):
    translated = GoogleTranslator(source='ru', target='en').translate(message.text)
    await message.answer(translated)



async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
