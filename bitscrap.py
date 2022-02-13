import requests
import logging
import fake_useragent
from bs4 import BeautifulSoup

# https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru


logging.basicConfig(level=logging.DEBUG,
					format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger(__name__)


class Valut:

	def responce_soup(self, link):
		try:
			user = fake_useragent.UserAgent(cache=False).random
			header = {'user-agent': user}

			responce = requests.get(link, headers=header).text
			soup = BeautifulSoup(responce, 'html.parser')

			return soup
		except Exception:
			logger.error("НЕ УДАЛОСЬ ПОДКЛЮЧИТЬСЯ К САЙТУ")
			breakpoint()

	def get_bit(self):
		link = f'https://www.rbc.ru/crypto/currency/btcusd'
		soup = self.responce_soup(link)

		bit = soup.find("div", class_="chart__subtitle js-chart-value")

		bit = bit.text.replace(' ', '')
		bit = bit.split('\n')

		logger.info('Запрос на стоимость биткоина выполнен')

		return f'стоимость биткоина - {bit[1]} $'

	def get_eth(self):
		link = f'https://www.rbc.ru/crypto/currency/ethusd'
		soup = self.responce_soup(link)

		eth = soup.find("div", class_="chart__subtitle js-chart-value")

		eth = eth.text.replace(' ', '')
		eth = eth.split('\n')

		logger.info('Запрос на стоимость эфириума выполнен')

		return f'стоимость эфириума - {eth[1]} $'

	def get_usd(self):
		link = f'https://quote.rbc.ru/ticker/72413'
		soup = self.responce_soup(link)

		usd = soup.find("span", class_="chart__info__sum")

		usd = usd.text.split(',')

		logger.info('Запрос на стоимость доллара выполнен')

		return f'стоимость доллара - {usd[0]} рублей'

	def get_eur(self):
		link = f'https://quote.rbc.ru/ticker/72383'
		soup = self.responce_soup(link)

		eur = soup.find("span", class_="chart__info__sum")

		eur = eur.text.split(',')

		logger.info('Запрос на стоимость евро выполнен')

		return f'стоимость евро - {eur[0]} рублей'
