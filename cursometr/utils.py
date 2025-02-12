import aiohttp
import json

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


async def get_crypto_data(contracts):
    result = []
    contracts = contracts.split()
    async with aiohttp.ClientSession() as session:
        for contract in contracts:
            crypto_data = fake_redis.get(contract)
            if not crypto_data:
                request = await session.get(
                    (
                        'https://api.coingecko.com/api/v3/coins/id/contract/'
                        f'{contract}'
                    )
                )
                if request.status not in (200, 304):
                    raise Exception('Сервис недоступен.')
                crypto_data = await request.text()
                crypto_data = json.loads(crypto_data)
                crypto_data = {
                    'name': crypto_data['name'],
                    'price': crypto_data['market_data']['current_price']['rub']
                }
                fake_redis[contract] = crypto_data
            result.append(crypto_data)
    return result


async def get_user_language(user_id):
    language_code = fake_redis.get(f'user{user_id}|lang_code')
    if not language_code:
        user = await ORM.get_user(user_id)
        language_code = user.language.value
        fake_redis[f'user{user_id}|lang_code'] = language_code
    return language_code
