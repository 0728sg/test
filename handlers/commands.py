from aiogram import types, Bot, Dispatcher
from aiogram.utils import executor
import os
from buttons import start
from config import bot


async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Hello!')
    await message.answer(text='Привет')


async def info_about_bot_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text='Here you can place an order')
    await message.answer(text='Here you can place an order')



def register_commands(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(info_about_bot_handler, commands=['bot_info'])