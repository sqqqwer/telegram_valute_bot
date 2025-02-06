from telebot import types

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
    ]])
    return keyboard
