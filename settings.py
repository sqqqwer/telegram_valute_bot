import os

from dotenv import load_dotenv


load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAMBOT_TOKEN')
DATABASE_NAME = 'db.sqlite'

current_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
voice_message_dir = current_dir + 'voicemessage/'
