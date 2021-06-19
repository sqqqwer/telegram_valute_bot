import requests
import fake_useragent
from bs4 import BeautifulSoup

# https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru 



class Valut:

	def get_bitok(self):
		#fake useragent
		user = fake_useragent.UserAgent().random
		header = {'user-agent': user}
		# site url/ссылка на сайт
		link = f'https://www.rbc.ru/crypto/currency/btcusd'
		# получение всего html кода / take html code from site
		responce = requests.get(link, headers=header).text
		soup = BeautifulSoup(responce, 'html.parser')
		# нахожу цену валюты / find cost of valute
		bit = soup.find("div", class_ = "chart__subtitle js-chart-value")

		# привожу полученный текст в нормальный вид
		# bring the resulting text into a normal form
		bit = bit.text.replace(' ', '')
		bit = bit.split('\n')
		
		return f'стоимость биткоина - {bit[1]}'

	def get_usd(self):
		user = fake_useragent.UserAgent().random
		header = {'user-agent': user}
		link = f'https://quote.rbc.ru/ticker/72413'

		responce = requests.get(link, headers=header).text
		soup = BeautifulSoup(responce, 'html.parser')

		usd = soup.find("span", class_ = "chart__info__sum")

		usd = usd.text.split(',')

		return f'стоимость доллара - {usd[0]}'

	def get_eur(self):
		user = fake_useragent.UserAgent().random
		header = {'user-agent': user}
		link = f'https://quote.rbc.ru/ticker/72383'

		responce = requests.get(link, headers=header).text
		soup = BeautifulSoup(responce, 'html.parser')

		eur = soup.find("span", class_ = "chart__info__sum")

		eur = eur.text.split(',')

		return f'стоимость евро - {eur[0]}'

