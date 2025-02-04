from telebot import types

REGISTER_STR = 'Зарегистрироваться'
VALUTE_STR = 'Валюты'
PROFILE_STR = 'Профиль'
CRIPTOVALITE_STR = 'Криптавалюты'
SUBSCRIBE = 'Подписаться на рассылку'
ABOUT_STR = 'О боте'


def keyboard_menu_register():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton(REGISTER_STR))
    return keyboard


def keyboard_menu_start():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton(VALUTE_STR),
        types.KeyboardButton(PROFILE_STR),
        types.KeyboardButton(CRIPTOVALITE_STR),
    )
    keyboard.row(
        types.KeyboardButton(SUBSCRIBE),
        types.KeyboardButton(ABOUT_STR)
    )
    return keyboard
