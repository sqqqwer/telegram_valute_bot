from sqlalchemy import select, update

from database.decorators import with_session
from database.models import Language, User


class ORM:

    @staticmethod
    @with_session
    async def add_user(
        chat_id: int,
        username: str,
        first_name: str,
        language_code: str,
        session
    ):
        new_user = User(
            chat_id=chat_id,
            language=language_code,
            username=username,
            first_name=first_name
        )
        session.add(new_user)
        await session.flush()
        await session.commit()

    @staticmethod
    @with_session
    async def get_user(chat_id, session):
        query = select(User).where(User.chat_id == chat_id)
        result = await session.execute(query)
        return result.scalars().first()

    @staticmethod
    @with_session
    async def change_user_language(chat_id, language, session):
        query = (
            update(User)
            .where(User.chat_id == chat_id)
            .values(language=Language[language])
        )
        await session.execute(query)
        await session.commit()
