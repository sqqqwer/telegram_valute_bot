import requests
import fake_useragent
from bs4 import BeautifulSoup

# https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru 


class Valut:

	def responce_soup(self, link):
		user = fake_useragent.UserAgent(cache=False).random
		header = {'user-agent': user}

		responce = requests.get(link, headers=header).text
		soup = BeautifulSoup(responce, 'html.parser')

		return soup

	def get_bit(self):
		link = f'https://www.rbc.ru/crypto/currency/btcusd'
		soup = self.responce_soup(link)

		bit = soup.find("div", class_="chart__subtitle js-chart-value")


		bit = bit.text
		# bit = bit[0] + ',' + bit[1].split(' ')[0]
		return bit
		# return f'стоимость биткоина - {bit} $'

	def get_eth(self):
		link = f'https://www.rbc.ru/crypto/currency/ethusd'
		soup = self.responce_soup(link)

		eth = soup.find("div", class_="chart__subtitle js-chart-value")

		eth = eth.text.split(',')
		eth = eth[0] + ',' + eth[1].split(' ')[0]

		return f'стоимость эфириума - {eth} $'

	def get_usd(self):
		link = f'https://quote.rbc.ru/ticker/72413'
		soup = self.responce_soup(link)

		usd = soup.find("span", class_="chart__info__sum")

		usd = usd.text.split(',')

		return f'стоимость доллара - {usd[0]} рублей'

	def get_eur(self):
		link = f'https://quote.rbc.ru/ticker/72383'
		soup = self.responce_soup(link)

		eur = soup.find("span", class_="chart__info__sum")

		eur = eur.text.split(',')

		return f'стоимость евро - {eur[0]} рублей'
