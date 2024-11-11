from telebot import types

VALUTE_STR = 'Валюты'
CRIPTOVALITE_STR = 'Криптавалюты'
SUBSCRIBE = 'Подписаться на рассылку'
ABOUT_STR = 'О боте'


def keyboard_menu_start():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton(VALUTE_STR),
        types.KeyboardButton(CRIPTOVALITE_STR)
    )
    keyboard.row(
        types.KeyboardButton(SUBSCRIBE),
        types.KeyboardButton(ABOUT_STR)
    )
    return keyboard
