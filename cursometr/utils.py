import aiohttp

from database.orm import ORM
from fake_redis import fake_redis
# Потом поменять на насоящий редис


def handle_button_message(message, button):
    return message.text in button


async def get_valutes():
    valutes_data = fake_redis.get('valute')
    if not valutes_data:
        async with aiohttp.ClientSession() as session:
            request = await session.get(
                'https://www.cbr-xml-daily.ru/daily_json.js'
            )
            if request.status != 200:
                raise Exception('Сервис недоступен.')
            valutes_data = await request.text()
            valutes_data = eval(valutes_data)['Valute']
            fake_redis['valute'] = valutes_data
    return valutes_data


async def get_user_language(user_id):
    language_code = fake_redis.get(f'user{user_id}|lang_code')
    if not language_code:
        user = await ORM.get_user(user_id)
        language_code = user.language.value
        fake_redis[f'user{user_id}|lang_code'] = language_code
    return language_code
