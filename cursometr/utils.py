import json

import asyncio
import aiohttp

from database.orm import ORM
from exceptions import BadRequest, NotExist404
from fake_redis import fake_redis
from settings import (CRYPTO_CONTRACTS_PLACES, CRYPTO_ENDPOINT_COINS_ID,
                      CRYPTO_ENDPOINT_CONTRACTS, CRYPTO_STANDART_COIN_ID)

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


async def get_single_crypto_api_data(endpoint, crypto_id):
    crypto_data = fake_redis.get(crypto_id)
    if not crypto_data:
        async with aiohttp.ClientSession() as session:
            request = await session.get(endpoint + crypto_id)
            if request.status == 404:
                raise NotExist404('Валюта не найдена.')
            if request.status not in (200, 304):
                raise await BadRequest('Сервис недоступен.')
            crypto_data = await request.text()
            crypto_data = json.loads(crypto_data)
            crypto_data = {
                'name': crypto_data['name'],
                'price': crypto_data['market_data']['current_price']['rub']
            }
            fake_redis[crypto_id] = crypto_data
    return crypto_data


async def _get_static_crypto_data():
    result = []
    static_crypto_id = CRYPTO_STANDART_COIN_ID
    for crypto_id in static_crypto_id:
        result.append(
            await get_single_crypto_api_data(
                CRYPTO_ENDPOINT_COINS_ID,
                crypto_id
            )
        )
    return result


async def get_crypto_data(contracts):
    contracts = contracts.split()
    result = await _get_static_crypto_data()

    contracts_data = []
    for contract in contracts:
        errors404 = 0
        for place_id in CRYPTO_CONTRACTS_PLACES:
            try:
                crypto_data = await asyncio.create_task(
                    get_single_crypto_api_data(
                        CRYPTO_ENDPOINT_CONTRACTS.format(place_id),
                        contract
                    )
                )
                contracts_data.append(crypto_data)
                break
            except NotExist404:
                errors404 += 1
        if errors404 == len(CRYPTO_CONTRACTS_PLACES):
            raise NotExist404('Валюта не найдена.')

    result.extend(contracts_data)
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
