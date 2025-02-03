import asyncio

from database.orm import ORM
from settings import TELEGRAM_BOT_TOKEN
from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
async def start_message(message):
    await bot.send_message(
        message.chat.id,
        'Напишите команду /register для регистрации.'
    )


@bot.message_handler(commands=['register'])
async def register(message):
    if message.from_user.is_bot:
        return await bot.send_message(
            message.chat.id,
            'Ботам регистрироваться нельзя!'
        )
    user = await ORM.get_user(message.from_user.id)
    if user:
        return await bot.send_message(
            message.chat.id,
            'Вы уже зарегистрированы!'
        )
    await ORM.add_user(
        chat_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        language_code=message.from_user.language_code
    )
    return await bot.send_message(
            message.chat.id,
            'Вы зарегестрированы! Можете пользоваться ботом!'
        )


@bot.message_handler(commands=['get_user'])
async def get_user(message):
    user = await ORM.get_user(message.from_user.id)
    if not user:
        return await bot.send_message(
            message.chat.id,
            'Вы незарегестрированы! Напишите команду /start'
        )
    await bot.send_message(message.chat.id, f'вы {user.username}')


asyncio.run(bot.polling(interval=2))
