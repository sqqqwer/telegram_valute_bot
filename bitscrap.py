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
		threading.Timer(20, self.parse_eth).start()
		threading.Timer(20, self.parse_usd).start()
		threading.Timer(20, self.parse_eur).start()
		logger.info('Парсинг данных выполнен')

		threading.Timer(600, self.parse).start()

	def responce_soup(self):
		try:
			user = user_agent.generate_user_agent()
			header = {
				'user-agent': user
			}

			link = f'https://www.profinance.ru/_quote_show_/java/'

			responce = requests.get(link, headers=header, timeout=18).text
			soup = BeautifulSoup(responce, 'html.parser')

			return soup
		except Exception:
			logger.error("НЕ УДАЛОСЬ ПОДКЛЮЧИТЬСЯ К САЙТУ")
			breakpoint()

	def parse_bit(self):
		soup = self.responce_soup()

		bit = soup.find("td", id="b_XBT_USD").text

		logger.info('Стоимость биткоина считана')

		return bit

	def parse_eth(self):
		soup = self.responce_soup()

		eth = soup.find("td", id="b_423").text

		logger.info('Стоимость эфириума считана')

		return eth

	def parse_usd(self):
		soup = self.responce_soup()

		usd = soup.find("td", id="b_29").text

		logger.info('Стоимость доллара считана')

		return usd

	def parse_eur(self):
		soup = self.responce_soup()

		eur = soup.find("td", id="b_30").text

		logger.info('Стоимость евро считана')

		return eur
