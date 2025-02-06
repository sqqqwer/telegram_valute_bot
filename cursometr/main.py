import asyncio

from telebot.async_telebot import AsyncTeleBot

from database.orm import ORM
from keyboards import (LOCALES, keyboard_menu_base, keyboard_menu_register)
from settings import TELEGRAM_BOT_TOKEN
from utils import get_valutes

bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
async def start_message(message):
    await bot.send_message(
        message.chat.id,
        'Нажмите кнопку  для регистрации.',
        reply_markup=keyboard_menu_register('ru')
    )


@bot.callback_query_handler(
        func=lambda call: call.data == LOCALES['REGISTER']['callback']
)
async def register(call):
    if call.from_user.is_bot:
        return await bot.edit_message_text(
            'Ботам регистрироваться нельзя!',
            chat_id=call.from_user.id, message_id=call.message.message_id
        )
    user = await ORM.get_user(call.from_user.id)
    if user:
        return await bot.edit_message_text(
            'Вы уже зарегистрированы!',
            reply_markup=keyboard_menu_base('ru'),
            chat_id=call.from_user.id, message_id=call.message.message_id
        )
    await ORM.add_user(
        chat_id=call.from_user.id,
        username=call.from_user.username,
        first_name=call.from_user.first_name,
        language_code=call.from_user.language_code
    )
    return await bot.edit_message_text(
            'Вы зарегестрированы! Можете пользоваться ботом!',
            reply_markup=keyboard_menu_base('ru'),
            chat_id=call.from_user.id, message_id=call.message.message_id
        )


@bot.callback_query_handler(
        func=lambda call: call.data == LOCALES['PROFILE']['callback']
)
async def get_profile(call):
    user = await ORM.get_user(call.from_user.id)
    await bot.edit_message_text(
        f'вы {user.username}',
        reply_markup=keyboard_menu_base('ru'),
        chat_id=call.from_user.id, message_id=call.message.message_id
    )


@bot.callback_query_handler(
        func=lambda call: call.data == LOCALES['VALUTE']['callback']
)
async def get_valute(call):
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

    await bot.edit_message_text(
        message_to_send,
        reply_markup=keyboard_menu_base('ru'),
        chat_id=call.from_user.id, message_id=call.message.message_id
    )


try:
    asyncio.run(bot.polling(interval=2))
except Exception as error:
    print(error)
