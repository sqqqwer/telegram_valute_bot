import os
import pathlib

from dotenv import load_dotenv


load_dotenv()

CURRENT_DIR = pathlib.Path(__file__).parent.resolve()
PROHECT_DIR = CURRENT_DIR.parent.resolve()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAMBOT_TOKEN')
DATABASE_NAME = 'db.sqlite'
DATABASE_URL = f'sqlite+aiosqlite:///{PROHECT_DIR}/{DATABASE_NAME}'
