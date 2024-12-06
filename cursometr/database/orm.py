from database.database import session_factory
from database.models import User


class ORM:
    @staticmethod
    async def add_user(
        chat_id: int,
        username: str,
        first_name: str,
        language_code: str
    ):
        async with session_factory() as session:
            new_user = User(
                chat_id=chat_id,
                language=language_code,
                username=username,
                first_name=first_name
            )
            session.add(new_user)
            await session.flush()
            await session.commit()
