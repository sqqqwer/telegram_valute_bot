import os
import telebot
import time

from fuzzywuzzy import fuzz

from pyffmpeg import FFmpeg
import speech_recognition as sr

from bitscrap import Valut
from config import TOKEN, voice_message_dir


recognizer = sr.Recognizer()
ff = FFmpeg()
bot = telebot.TeleBot(TOKEN)
valut = Valut()


@bot.message_handler(commands=['start', 'help'])
def show_command_list(message):
	bot.send_message(message.chat.id, '''Commands:
	/help - show all commands
	/btk - show bitcoin
	/eth - show ethereum
	/usd - show usd
	/eur - show eur
	/all - show all valuts
	/author - show author''')


@bot.message_handler(commands=['all'])
def show_all_valut(message):
	bot.send_message(message.chat.id, valut.get_bit())
	bot.send_message(message.chat.id, valut.get_eth())
	bot.send_message(message.chat.id, valut.get_usd())
	bot.send_message(message.chat.id, valut.get_eur())


@bot.message_handler(commands=['author'])
def show_author(message):
	bot.send_message(message.chat.id, 'Автор этого бота это - sqqqwer(Чернявский Владислав)')


@bot.message_handler(commands=['btk'])
def show_bitcoin(message):
	bot.send_message(message.chat.id, valut.get_bit())


@bot.message_handler(commands=['eth'])
def show_ethereum(message):
	bot.send_message(message.chat.id, valut.get_eth())


@bot.message_handler(commands=['usd'])
def show_usd(message):
	bot.send_message(message.chat.id, valut.get_usd())


@bot.message_handler(commands=['eur'])
def show_eur(message):
	bot.send_message(message.chat.id, valut.get_eur())


@bot.message_handler(content_types=['voice'])
def voice_response(message):
	try:
		file_id = bot.get_file(message.voice.file_id)
		voice_file = bot.download_file(file_id.file_path)

		voice_file_path = voice_message_dir + str(file_id.file_unique_id)+".ogg"

		with open(voice_file_path, 'wb') as new_file:
			new_file.write(voice_file)

		bot.reply_to(message, "Сообщение анализируется. Подождите...")
		time.sleep(2)

		converted_voice_file_path = voice_message_dir + str(file_id.file_unique_id)+"wavedition.wav"

		ff.convert(voice_file_path, converted_voice_file_path)

		with sr.WavFile(converted_voice_file_path) as voiceFile:
			audio = recognizer.record(voiceFile)

		query = recognizer.recognize_google(audio, language="ru-RU", show_all=False).lower()

		os.remove(voice_file_path)
		os.remove(converted_voice_file_path)

		bot.reply_to(message, query)

		# сравнение полученного текста и ключевых слов
		# comparison of the received text from keywords
		hello = ['привет']
		if fuzz.WRatio(hello, query) >= 80:
			bot.send_message(message.chat.id, 'привет я робот')

		namess = ['меня зовут']
		if fuzz.WRatio(namess, query) >= 80:
			name_user = query.split('зовут')
			bot.send_message(message.chat.id, f'приятно познакомиться, {name_user[1]}')

		bitc = ['биткоин', 'bitcoin', 'биткоин']
		if fuzz.WRatio(bitc, query) >= 58:
			bot.send_message(message.chat.id, valut.get_bit())

		eth = ['эфириум', 'ethereum', 'ифириум']
		if fuzz.WRatio(eth, query) >= 58:
			bot.send_message(message.chat.id, valut.get_eth())

		eur = ['евро']
		if fuzz.WRatio(eur, query) >= 58:
			bot.send_message(message.chat.id, valut.get_eur())

		usd = ['доллар']
		if fuzz.WRatio(usd, query) >= 58:
			bot.send_message(message.chat.id, valut.get_usd())

	except Exception as error:
		bot.reply_to(message, "Произошла ошибка...")
		print(error)


valut.start_parse_loop()
bot.polling(none_stop=True)
