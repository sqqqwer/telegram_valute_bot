import aiohttp
import json

from database.orm import ORM
from fake_redis import fake_redis
from settings import CRYPTO_ENDPOINT_COINS_ID, CRYPTO_ENDPOINT_CONTRACTS
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


async def get_single_crypto_api_data(endpoint, crypto_id_list):
    result = []
    for crypto_id in crypto_id_list:
        crypto_data = fake_redis.get(crypto_id)
        if not crypto_data:
            async with aiohttp.ClientSession() as session:
                request = await session.get(endpoint + crypto_id)
                if request.status not in (200, 304):
                    raise Exception('Сервис недоступен.')
                crypto_data = await request.text()
                crypto_data = json.loads(crypto_data)
                crypto_data = {
                    'name': crypto_data['name'],
                    'price': crypto_data['market_data']['current_price']['rub']
                }
                fake_redis[crypto_id] = crypto_data
        result.append(crypto_data)
    return result


async def _get_static_crypto_data():
    static_crypto_id = ('bitcoin', 'ethereum')
    result = await get_single_crypto_api_data(
        CRYPTO_ENDPOINT_COINS_ID,
        static_crypto_id
        )
    return result


async def get_crypto_data(contracts):
    result = []
    contracts = contracts.split()
    result = await _get_static_crypto_data()
    crypto_data = await get_single_crypto_api_data(
        CRYPTO_ENDPOINT_CONTRACTS,
        contracts
    )
    result.extend(crypto_data)
    return result


async def get_user_language_field(user_id):
    language_code = fake_redis.get(f'user{user_id}|lang_code')
    if not language_code:
        user = await ORM.get_user(user_id)
        language_code = user.language.value
        fake_redis[f'user{user_id}|lang_code'] = language_code
    return language_code


async def get_user_crypto_field(user_id):
    crypto = fake_redis.get(f'user{user_id}|crypto')
    if not crypto:
        user = await ORM.get_user(user_id)
        crypto = user.crypto
        fake_redis[f'user{user_id}|crypto'] = crypto
    return crypto
