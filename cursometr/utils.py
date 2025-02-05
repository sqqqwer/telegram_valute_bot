import aiohttp

# Потом поменять на редис
fake_redis = {}


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
