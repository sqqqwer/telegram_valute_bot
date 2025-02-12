import enum

from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base
from settings import ETHEREUM_CONTRACT


class Language(enum.Enum):
    en = 'en'
    ru = 'ru'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
    language: Mapped[Language]
    username: Mapped[str]
    first_name: Mapped[str]
    valutes: Mapped[str] = mapped_column(default='USD EUR ')
    crypto: Mapped[str] = mapped_column(default=ETHEREUM_CONTRACT)
