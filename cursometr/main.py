import asyncio

from telebot.async_telebot import AsyncTeleBot

from database.orm import ORM
from keyboards import (PROFILE_STR, REGISTER_STR, keyboard_menu_register,
                       keyboard_menu_start, VALUTE_STR)
from settings import TELEGRAM_BOT_TOKEN
from utils import handle_button_message, get_valutes

bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
async def start_message(message):
    await bot.send_message(
        message.chat.id,
        'Нажмите кнопку  для регистрации.',
        reply_markup=keyboard_menu_register()
    )


@bot.message_handler(
        func=lambda message: handle_button_message(message, REGISTER_STR)
)
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
            'Вы уже зарегистрированы!',
            reply_markup=keyboard_menu_start()
        )
    await ORM.add_user(
        chat_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        language_code=message.from_user.language_code
    )
    return await bot.send_message(
            message.chat.id,
            'Вы зарегестрированы! Можете пользоваться ботом!',
            reply_markup=keyboard_menu_start()
        )


@bot.message_handler(
        func=lambda message: handle_button_message(message, PROFILE_STR)
)
async def get_profile(message):
    user = await ORM.get_user(message.from_user.id)
    if not user:
        return await bot.send_message(
            message.chat.id,
            'Вы незарегестрированы! Напишите команду /start'
        )
    await bot.send_message(message.chat.id, f'вы {user.username}')


@bot.message_handler(
        func=lambda message: handle_button_message(message, VALUTE_STR)
)
async def get_valute(message):
    valute = await get_valutes()

    message_to_send = ''
    need_valutes = ('USD', 'EUR')
    for code in need_valutes:
        valute_dict = valute[code]
        message_for_valute = (
            f"{valute_dict['Name']} -"
            f" {valute_dict['Value'] / valute_dict['Nominal']}\n"
        )
        message_to_send += message_for_valute

    await bot.send_message(message.chat.id, message_to_send)


try:
    asyncio.run(bot.polling(interval=2))
except Exception as error:
    print(error)
