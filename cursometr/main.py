import asyncio

from database.orm import ORM
from settings import TELEGRAM_BOT_TOKEN
from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
async def start_message(message):
    if not message.from_user.is_bot:
        print(message.from_user.id)
        print(message.from_user.username)
        print(message.from_user.first_name)
        print(message.from_user.language_code)
        await ORM.add_user(
            chat_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            language_code=message.from_user.language_code
        )

    await bot.send_message(message.chat.id, 'Добро пожаловать')

asyncio.run(bot.polling(interval=2))
