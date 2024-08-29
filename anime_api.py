import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random
import requests
from datetime import datetime, timedelta

from config import TOKEN, NASA_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_anime(text):
   url = f'https://kitsu.io/api/edge/anime?filter[text]={text}'
   response = requests.get(url)
   if response.status_code == 200:
      anime_data = response.json()
      if anime_data['data']:
         return anime_data['data'][0]  # Возвращаем информацию о первом найденном аниме
      else:
         return None
   else:
      return None

@dp.message(Command("start"))
async def start_command(message: Message):
   await message.answer("Привет! Напиши мне название anime, и я пришлю тебе её фото и описание.")

@dp.message()
async def send_cat_info(message: Message):
   anime_name = message.text
   anime_info = get_anime(anime_name)
   anime_info = get_anime(anime_name)
   if anime_info:
      title = anime_info['attributes']['canonicalTitle']
      synopsis = anime_info['attributes']['synopsis']
      show_type = anime_info['attributes']['showType']
      start_date = anime_info['attributes']['startDate']
      poster_image_url = anime_info['attributes']['posterImage']['medium']
      info = (
         f"Title: {title}\n"
         f"Type: {show_type}\n"
         f"Start Date: {start_date}\n"
         f"Synopsis: {synopsis}\n"

      )
      await message.answer_photo(photo=poster_image_url, caption=info)
   else:
      await message.answer("Аниме не найдено. Попробуйте еще раз.")

async def main():
   await dp.start_polling(bot)

if __name__ == '__main__':
   asyncio.run(main())

