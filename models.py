from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
    username: Mapped[str]
    first_name: Mapped[str]
