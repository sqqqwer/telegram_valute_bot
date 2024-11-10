from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from settings import DATABASE_NAME


engine = create_engine(f'sqlite:///{DATABASE_NAME}', echo=True)

session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
