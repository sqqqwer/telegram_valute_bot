import asyncio
from telebot.async_telebot import AsyncTeleBot
from settings import TELEGRAM_BOT_TOKEN


bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
async def start_message(message):
    print(message)
    await bot.send_message(message.chat.id, 'Добро пожаловать')


asyncio.run(bot.polling(interval=2))
