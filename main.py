import asyncio
from aiogram import Bot, Router, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command
from config import TOKEN
import random
from gtts import gTTS
import os
from deep_translator import GoogleTranslator





bot = Bot(token=TOKEN)
router = Router()

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
    '1'
    '2'
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

@router.message(Command('Weather'))
async def Weather(message: Message):
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
