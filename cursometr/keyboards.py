from telebot import types

from database.models import Language


LOCALES = {
    'REGISTER': {
        'callback': 'REGISTER',
        'en': 'Register',
        'ru': 'Зарегистрироваться'
    },
    'VALUTE': {
        'callback': 'VALUTE',
        'en': 'Valute',
        'ru': 'Валюты'
    },
    'PROFILE': {
        'callback': 'PROFILE',
        'en': 'Profile',
        'ru': 'Профиль'
    },
    'CRYPTOVALUTE': {
        'callback': 'CRYPTOVALUTE',
        'en': 'Cryptovalute',
        'ru': 'Криптовалюты'
    },
    'ABOUT': {
        'callback': 'ABOUT',
        'en': 'About bot',
        'ru': 'О Боте'
    },
    'LANGUAGE': {
        'callback': 'LANGUAGE',
        'en': '🌍',
        'ru': '🌍'
    },
    'LANGUAGE_CHOISE': {
        'callback': 'LANGUAGE_CHOISE',
        'en': '🇬🇧',
        'ru': '🇷🇺'
    },
}


def keyboard_menu_register(language_code):
    keyboard = types.InlineKeyboardMarkup([[
        types.InlineKeyboardButton(
            LOCALES['REGISTER'][language_code],
            callback_data=LOCALES['REGISTER']['callback']
        ),
    ]])
    return keyboard


def keyboard_menu_base(language_code):
    keyboard = types.InlineKeyboardMarkup([[
        types.InlineKeyboardButton(
            LOCALES['VALUTE'][language_code],
            callback_data=LOCALES['VALUTE']['callback']
        ),
        types.InlineKeyboardButton(
            LOCALES['CRYPTOVALUTE'][language_code],
            callback_data=LOCALES['CRYPTOVALUTE']['callback']
        ),
        types.InlineKeyboardButton(
            LOCALES['PROFILE'][language_code],
            callback_data=LOCALES['PROFILE']['callback']
        ),
        types.InlineKeyboardButton(
            LOCALES['LANGUAGE'][language_code],
            callback_data=LOCALES['LANGUAGE']['callback']
        ),
    ]])
    return keyboard


def keyboard_menu_language():
    inline_keys = []
    for item in LOCALES['LANGUAGE_CHOISE'].items():
        if item[0] == 'callback':
            continue
        inline_keys.append(
            types.InlineKeyboardButton(
                item[1],
                callback_data=str({
                    'callback': LOCALES['LANGUAGE_CHOISE']['callback'],
                    'language': Language[item[0]].value
                })
            )
        )
    keyboard = types.InlineKeyboardMarkup([inline_keys])
    return keyboard
