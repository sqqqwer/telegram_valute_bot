import asyncio

from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import StateFilter
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup

from database.orm import ORM
from keyboards import (LOCALES, keyboard_menu_base, keyboard_menu_crypto_edit,
                       keyboard_menu_language, keyboard_menu_register,
                       keyboard_menu_settings)
from settings import CRYPTO_ENDPOINT_CONTRACTS, TELEGRAM_BOT_TOKEN
from utils import (get_single_crypto_api_data, get_user_crypto_field, get_user_language_field,
                   get_valutes, get_crypto_data)

bot = AsyncTeleBot(TELEGRAM_BOT_TOKEN, state_storage=StateMemoryStorage())

class AddStates(StatesGroup):
    crypto_contract = State()
    valute_code = State()


@bot.message_handler(commands=['start'])
async def start_message(message):
    await bot.send_message(
        message.chat.id,
        'Нажмите кнопку  для регистрации.',
        reply_markup=keyboard_menu_register(message.from_user.language_code)
    )


@bot.callback_query_handler(
        func=lambda call: call.data == LOCALES['REGISTER']['callback']
)
async def register(call):
    user = await ORM.get_user(call.from_user.id)
    if user:
        return await bot.edit_message_text(
            'Вы уже зарегистрированы!',
            reply_markup=keyboard_menu_base(user.language.value),
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
            reply_markup=keyboard_menu_base(call.from_user.language_code),
            chat_id=call.from_user.id, message_id=call.message.message_id
        )


@bot.callback_query_handler(
        func=lambda call: call.data == LOCALES['PROFILE']['callback']
)
async def get_profile(call):
    user = await ORM.get_user(call.from_user.id)
    await bot.edit_message_text(
        f'вы {user.username}',
        reply_markup=keyboard_menu_base(user.language.value),
        chat_id=call.from_user.id, message_id=call.message.message_id
    )


@bot.callback_query_handler(
        func=lambda call: call.data == LOCALES['VALUTE']['callback']
)
async def get_valute(call):
    valute = await get_valutes()
    language_code = await get_user_language_field(call.from_user.id)

    message_to_send = ''
    need_valutes = 'USD EUR '
    need_valutes = need_valutes.split()
    for code in need_valutes:
        valute_dict = valute[code]
        message_for_valute = (
            f"{valute_dict['Name']} -"
            f" {valute_dict['Value'] / valute_dict['Nominal']}\n"
        )
        message_to_send += message_for_valute

    await bot.edit_message_text(
        message_to_send,
        reply_markup=keyboard_menu_base(language_code),
        chat_id=call.from_user.id, message_id=call.message.message_id
    )


@bot.callback_query_handler(
        func=lambda call: call.data == LOCALES['CRYPTOVALUTE']['callback']
)
async def get_crypto(call):
    user = await ORM.get_user(call.from_user.id)
    need_crypto = user.crypto
    crypto_data = await get_crypto_data(need_crypto)

    message_to_send = ''
    for crypto in crypto_data:
        message_for_crypto = (
            f"{crypto['name']} -"
            f" {crypto['price']}\n"
        )
        message_to_send += message_for_crypto

    await bot.edit_message_text(
        message_to_send,
        reply_markup=keyboard_menu_base(user.language.value),
        chat_id=call.from_user.id, message_id=call.message.message_id
    )


@bot.callback_query_handler(
        func=lambda call: call.data == LOCALES['BACK']['callback']
)
async def get_base_keyboard(call):
    language_code = await get_user_language_field(call.from_user.id)

    await bot.edit_message_text(
        'Выберите действие:',
        reply_markup=keyboard_menu_base(language_code),
        chat_id=call.from_user.id, message_id=call.message.message_id
    )


@bot.callback_query_handler(
        func=lambda call: call.data == LOCALES['SETTINGS']['callback']
)
async def get_settings_keyboard(call):
    language_code = await get_user_language_field(call.from_user.id)

    await bot.edit_message_text(
        'Настройки:',
        reply_markup=keyboard_menu_settings(language_code),
        chat_id=call.from_user.id, message_id=call.message.message_id
    )


@bot.callback_query_handler(
        func=lambda call: call.data == LOCALES['LANGUAGE']['callback']
)
async def get_language_keyboard(call):
    # language_code = await get_user_language_field(call.from_user.id)

    await bot.edit_message_text(
        'Выберите язык:',
        reply_markup=keyboard_menu_language(),
        chat_id=call.from_user.id, message_id=call.message.message_id
    )


@bot.callback_query_handler(
        func=lambda call:
        call.data == LOCALES['CHOISECRYPTOVALUTE_ADD']['callback']
)
async def add_crypto_contract(call):
    # language_code = await get_user_language_field(call.from_user.id)
    await bot.set_state(
        call.from_user.id, AddStates.crypto_contract, call.from_user.id
    )
    await bot.edit_message_text(
        'Введите контракт Ethereum или BNB Smart Chain (BEP20):',
        chat_id=call.from_user.id, message_id=call.message.message_id
    )


@bot.message_handler(
        state=AddStates.crypto_contract
)
async def add_crypto_contract_write(message):
    await ORM.add_crypto_contract(message.chat.id, message.text)
    await bot.delete_state(message.from_user.id, message.chat.id)

    language_code = await get_user_language_field(message.from_user.id)
    crypto_contracts = await get_user_crypto_field(message.from_user.id)
    await bot.send_message(
        message.chat.id,
        'Контракт сохранён.',
        reply_markup=keyboard_menu_crypto_edit(
            language_code, crypto_contracts
        )
    )


@bot.callback_query_handler(
        func=lambda call:
        call.data == LOCALES['CHOISECRYPTOVALUTE_MENU']['callback']
)
async def get_displayed_crypto_keyboard(call):
    language_code = await get_user_language_field(call.from_user.id)
    crypto_contracts = await get_user_crypto_field(call.from_user.id)

    await bot.edit_message_text(
        'Удалите или добавьте новые контракты:',
        reply_markup=keyboard_menu_crypto_edit(
            language_code, crypto_contracts
        ),
        chat_id=call.from_user.id, message_id=call.message.message_id
    )


@bot.callback_query_handler(
        func=(lambda call:
              eval(call.data)['callback']
              == LOCALES['CHOISECRYPTOVALUTE_DELETE']['callback'])
)
async def delete_crypto_contract(call):
    crypto_contracts = await get_user_crypto_field(call.from_user.id)
    contract_id = eval(call.data)['contract_id']
    contract = crypto_contracts.split()[contract_id]

    language_code = await get_user_language_field(call.from_user.id)
    success = await ORM.delete_crypto_contract(call.from_user.id, contract)
    crypto_contracts = await get_user_crypto_field(call.from_user.id)

    message = f'Контракт {contract} удалён.\nВыберите действие:'

    if not success:
        message = f'Контракта {contract} не существует.\nВыберите действие:'

    await bot.edit_message_text(
        message,
        reply_markup=keyboard_menu_crypto_edit(
            language_code, crypto_contracts
        ),
        chat_id=call.from_user.id, message_id=call.message.message_id
    )


@bot.callback_query_handler(
        func=(lambda call:
              eval(call.data)['callback']
              == LOCALES['LANGUAGE_CHOISE']['callback'])
)
async def change_language(call):
    language_code = eval(call.data)['language']
    await ORM.change_user_language(call.from_user.id, language_code)

    await bot.edit_message_text(
        'Язык изменён',
        reply_markup=keyboard_menu_base(language_code),
        chat_id=call.from_user.id, message_id=call.message.message_id
    )


bot.add_custom_filter(StateFilter(bot))

try:
    asyncio.run(bot.polling(interval=2))
except Exception as error:
    print(error)
