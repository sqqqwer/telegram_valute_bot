import os
import telebot
import time

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from pyffmpeg import FFmpeg
import speech_recognition as sr

from bitscrap import Valut
from config import TOKEN, current_dir


recognizer = sr.Recognizer()
ff = FFmpeg()
valut = Valut()

# инициализирование бота/bot initialization 
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def bitpokaz(message):
	bot.send_message(message.chat.id,'''Commands:
	/help - show all commands
	/btk - show bitcoin
	/usd - show usd
	/eur - show eur
	/all - show all valute
	/author - show author''')



@bot.message_handler(commands=['all'])
def bitpokaz(message):
	print('произошла обработка показа всех валют')

	bot.send_message(message.chat.id, valut.get_bitok() )
	bot.send_message(message.chat.id, valut.get_usd() )
	bot.send_message(message.chat.id, valut.get_eur() )

#показ биткоина
@bot.message_handler(commands=['btk'])
def bitpokaz(message):
	print('произошла обработка показа биткоина')
	bot.send_message(message.chat.id, valut.get_bitok() )


@bot.message_handler(commands=['author'])
def bitpokaz(message):
	bot.send_message(message.chat.id, 'Автор этого бота это - sqqqwer(я)' )

#показ доллара
@bot.message_handler(commands=['usd'])
def bitpokaz(message):
	bot.send_message(message.chat.id, valut.get_usd() )

#показ евро
@bot.message_handler(commands=['eur'])
def bitpokaz(message):
	bot.send_message(message.chat.id, valut.get_eur() )


# при появлении голосового сообщения используется функция otvet_na_voice
@bot.message_handler(content_types=['voice'])
def otvet_na_voice(message):
	try:
		#получение файла/getting file
		file_info = bot.get_file(message.voice.file_id)
		#Скачивание файла/download file
		downloaded_file = bot.download_file(file_info.file_path)
		#путь для скачки файла/path to downloaded file
		src = current_dir+'voicemessage/'+str(file_info.file_unique_id)+".ogg"
		#создание скачаного файла/creating downloaded file
		with open(src, 'wb') as new_file:
			new_file.write(downloaded_file)

		#предупреждения пользователя/
		bot.reply_to(message, "Сообщение анализируется. Подождите...")
		time.sleep(2)
		#путь для конвертириемого файла/path for convert file
		link = current_dir+'voicemessage/'+str(file_info.file_unique_id)+"wavedition.wav"
		#конвертация/converting
		output_file = ff.convert(src, link)
		#открытие и рекорд конвер файла/creating converted file
		with sr.WavFile(link) as voiceFile:
			audio = recognizer.record(voiceFile)
		#дебаг принт/dubug print
		print('аудио сообщение обработалось')

		#воспринятие голоса роботом гугла/voice perception by google robot 
		querye = recognizer.recognize_google(audio, language="ru-RU",show_all=False).lower()

		#удаление ненужных файлов/deleting unnecessary files 
		os.remove(src)
		os.remove(link)
		#реплай голосового сообщения и вывод текста произнесённого в голосовом сообщении
		#replay a voice message and output the text spoken in a voice message 
		bot.reply_to(message, querye)


		#сравнение полученного текста из ключевых слов
		#comparison of the received text from keywords 
		hello = ['привет']
		if fuzz.WRatio(hello, querye) >= 80  :
			bot.send_message(message.chat.id, 'привет я робот' )

		namess = ['меня зовут']
		if fuzz.WRatio(namess, querye) >= 80:
			name_user = querye.split('зовут')
			bot.send_message(message.chat.id, f'приятно познакомиться, {name_user[1]}')

		bitc = ['биткоин', 'bitcoin',]
		if fuzz.WRatio(bitc, querye) >= 65:
			bot.send_message(message.chat.id, valut.get_bitok())

		eur = ['евро', 'euro']
		if fuzz.WRatio(eur, querye) >= 65:
			bot.send_message(message.chat.id, valut.get_eur())

		usd = ['доллар', 'dollar']
		if fuzz.WRatio(usd, querye) >= 65:
			bot.send_message(message.chat.id, valut.get_usd())

	except Exception as error:
		#сообщение при ошибке
		bot.reply_to(message, error)
		print(error)
		#bot.reply_to(message, error)

#запуск бота/turn on bot
bot.polling(none_stop=True)

