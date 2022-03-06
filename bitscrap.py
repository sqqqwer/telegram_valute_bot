import requests
import threading
import logging

import user_agent

from bs4 import BeautifulSoup

# https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru


logging.basicConfig(level=logging.DEBUG,
					format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger(__name__)


class Valut:

	bit_value = 0
	eth_value = 0
	usd_value = 0
	eur_value = 0

	def get_bit(self):
		return f'стоимость биткоина - {self.bit_value} $'

	def get_eth(self):
		return f'стоимость эфириума - {self.eth_value} $'

	def get_usd(self):
		return f'стоимость доллара - {self.usd_value} рублей'

	def get_eur(self):
		return f'стоимость евро - {self.eur_value} рублей'

	def start_parse_loop(self):
		self.parse()

	def parse(self):
		threading.Timer(2, self.parse_bit).start()
		threading.Timer(60, self.parse_eth).start()
		threading.Timer(60, self.parse_usd).start()
		threading.Timer(60, self.parse_eur).start()
		logger.info('Парсинг данных выполнен')

		threading.Timer(600, self.parse).start()

	def responce_soup(self, link):
		try:
			user = user_agent.generate_user_agent()
			header = {'user-agent': user}

			responce = requests.get(link, headers=header, timeout=30).text
			soup = BeautifulSoup(responce, 'html.parser')

			return soup
		except Exception:
			logger.error("НЕ УДАЛОСЬ ПОДКЛЮЧИТЬСЯ К САЙТУ")
			breakpoint()

	def parse_bit(self):
		link = f'https://www.rbc.ru/crypto/currency/btcusd'
		soup = self.responce_soup(link)

		bit = soup.find("div", class_="chart__subtitle js-chart-value")

		bit = bit.text.replace(' ', '')
		bit = bit.split('\n')

		logger.info('Стоимость биткоина считана')

		return bit[1]

	def parse_eth(self):
		link = f'https://www.rbc.ru/crypto/currency/ethusd'
		soup = self.responce_soup(link)

		eth = soup.find("div", class_="chart__subtitle js-chart-value")

		eth = eth.text.replace(' ', '')
		eth = eth.split('\n')

		logger.info('Стоимость эфириума считана')

		return eth[1]

	def parse_usd(self):
		link = f'https://quote.rbc.ru/ticker/72413'
		soup = self.responce_soup(link)

		usd = soup.find("span", class_="chart__info__sum")

		usd = usd.text.split(',')

		logger.info('Стоимость доллара считана')

		return usd[0]

	def parse_eur(self):
		link = f'https://quote.rbc.ru/ticker/72383'
		soup = self.responce_soup(link)

		eur = soup.find("span", class_="chart__info__sum")

		eur = eur.text.split(',')

		logger.info('Стоимость евро считана')

		return eur[0]
