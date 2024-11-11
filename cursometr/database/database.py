from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from settings import DATABASE_URL


engine = create_engine(DATABASE_URL, echo=True)

session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
