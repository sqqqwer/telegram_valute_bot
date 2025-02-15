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
    'SETTINGS': {
        'callback': 'SETTINGS',
        'en': 'Settings',
        'ru': 'Настройки'
    },
    'CHOISEVALUTE': {
        'callback': 'CHOISEVALUTE',
        'en': 'Select the displayed VALUTE',
        'ru': 'Выбрать отображаемые Валюты'
    },
    'CHOISECRYPTOVALUTE_MENU': {
        'callback': 'CHOISECRYPTOVALUTE',
        'en': 'Select the displayed CRYPTO',
        'ru': 'Выбрать отображаемые Криптовалюты'
    },
    'CHOISECRYPTOVALUTE_ADD': {
        'callback': 'CHOISECRYPTOVALUTE_ADD',
        'en': 'Add new ➕',
        'ru': 'Добавить ➕'
    },
    'BACK': {
        'callback': 'BACK',
        'en': 'Back',
        'ru': 'Назад'
    },
    'CHOISECRYPTOVALUTE_DELETE': {
        'callback': 'CHOISECRYPTOVALUTE_DELETE',
        'en': 'Delete 🗑️',
        'ru': 'Удалить 🗑️'
    }
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
        )
    ], [
        types.InlineKeyboardButton(
            LOCALES['PROFILE'][language_code],
            callback_data=LOCALES['PROFILE']['callback']
        ),
        types.InlineKeyboardButton(
            LOCALES['LANGUAGE'][language_code],
            callback_data=LOCALES['LANGUAGE']['callback']
        ),
        types.InlineKeyboardButton(
            LOCALES['SETTINGS'][language_code],
            callback_data=LOCALES['SETTINGS']['callback']
        ),
    ]
    ])
    return keyboard


def keyboard_menu_settings(language_code):
    keyboard = types.InlineKeyboardMarkup([[
        types.InlineKeyboardButton(
            LOCALES['CHOISEVALUTE'][language_code],
            callback_data=LOCALES['CHOISEVALUTE']['callback']
        )
    ], [
        types.InlineKeyboardButton(
            LOCALES['CHOISECRYPTOVALUTE_MENU'][language_code],
            callback_data=LOCALES['CHOISECRYPTOVALUTE_MENU']['callback']
        )
    ], [
        types.InlineKeyboardButton(
            LOCALES['BACK'][language_code],
            callback_data=LOCALES['BACK']['callback']
        )
    ]
    ])
    return keyboard


def keyboard_menu_crypto_edit(language_code, contracts):
    contracts = contracts.split()
    inline_keys = []

    for i in range(len(contracts)):
        inline_keys.append(
            [
                types.InlineKeyboardButton(
                    contracts[i],
                    callback_data='no_data'
                ),
                types.InlineKeyboardButton(
                    LOCALES['CHOISECRYPTOVALUTE_DELETE'][language_code],
                    callback_data=str({
                        'callback': LOCALES[
                            'CHOISECRYPTOVALUTE_DELETE']['callback'],
                        'contract_id': i
                    })
                ),
            ]
        )
    inline_keys.extend(
        [
            [
                types.InlineKeyboardButton(
                    LOCALES['CHOISECRYPTOVALUTE_ADD'][language_code],
                    callback_data=LOCALES['CHOISECRYPTOVALUTE_ADD']['callback']
                )
            ],
            [
                types.InlineKeyboardButton(
                    LOCALES['BACK'][language_code],
                    callback_data=LOCALES['BACK']['callback']
                )
            ]
        ]
    )
    keyboard = types.InlineKeyboardMarkup(inline_keys)

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
