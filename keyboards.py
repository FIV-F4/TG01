from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Привет'),

    ],
    [
        KeyboardButton(text='Пока'),
    ]
], resize_keyboard=True)

inline_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Музыка', url=f"https://example.com/music"),
    ],
    [
        InlineKeyboardButton(text='Новости', url=f"https://example.com/news"),
        InlineKeyboardButton(text='Видео', url=f"https://example.com/video"),
    ]
])

inline_keyboard_test2 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Показать больше', callback_data="dynamic1"),
    ]
])

inline_keyboard_test3 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Опция 1', callback_data="dynamic1_1"),
        InlineKeyboardButton(text='Опция 2', callback_data="dynamic1_2"),
    ]
])


test = ["1","2","3","4"]

async def test_keyboard():
    keyboard = InlineKeyboardBuilder()
    for i in test:
        keyboard.add(InlineKeyboardButton(text=i, url=f"https://example.com/{i}"))
    #keyboard.adjust(3)
    return keyboard.adjust(2).as_markup()
'''
async def test_keyboard():
    keyboard = ReplyKeyboardBuilder()
    for i in test:
        keyboard.add(KeyboardButton(text=i))
    #keyboard.adjust(3)
    return keyboard.adjust(2).as_markup()
'''