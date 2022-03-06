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
		return f'стоимость биткоина - {self.bit_value}'

	def get_eth(self):
		return f'стоимость эфириума - {self.eth_value}'

	def get_usd(self):
		return f'стоимость доллара - {self.usd_value}'

	def get_eur(self):
		return f'стоимость евро - {self.eur_value}'

	def start_parse_loop(self):
		self.parse()

	def parse(self):
		self.bit_value = self.parse_bit()
		self.eth_value = self.parse_eth()
		self.usd_value = self.parse_usd()
		self.eur_value = self.parse_eur()
		logger.info('Парсинг данных выполнен')

		threading.Timer(600, self.parse).start()

	def responce_soup(self, link):
		try:
			user = user_agent.generate_user_agent()
			header = {
				'user-agent': user
			}

			responce = requests.get(link, headers=header, timeout=15).text
			soup = BeautifulSoup(responce, 'html.parser')

			return soup
		except Exception:
			logger.error("НЕ УДАЛОСЬ ПОДКЛЮЧИТЬСЯ К САЙТУ")
			breakpoint()

	def parse_bit(self):
		link = f'https://www.finanz.ru/valyuty/btc-usd'
		soup = self.responce_soup(link)

		bit = soup.find_all('div', class_="content")[1]
		bit = bit.find('th').text

		logger.info('Стоимость биткоина считана')
		return bit

	def parse_eth(self):
		link = f'https://www.finanz.ru/valyuty/eth-usd'
		soup = self.responce_soup(link)

		eth = soup.find_all('div', class_="content")[1]
		eth = eth.find('th').text

		logger.info('Стоимость эфириума считана')
		return eth

	def parse_usd(self):
		link = f'https://www.finanz.ru/valyuty/usd-rub'
		soup = self.responce_soup(link)

		usd = soup.find_all('div', class_="content")[1]
		usd = usd.find('th').text

		logger.info('Стоимость доллара считана')
		return usd

	def parse_eur(self):
		link = f'https://www.finanz.ru/valyuty/eur-rub'
		soup = self.responce_soup(link)

		eur = soup.find_all('div', class_="content")[1]
		eur = eur.find('th').text

		logger.info('Стоимость евро считана')
		return eur
