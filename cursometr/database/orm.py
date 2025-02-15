from sqlalchemy import select, update

from database.decorators import with_session
from database.models import Language, User
from fake_redis import fake_redis


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
        fake_redis[f'user{chat_id}|lang_code'] = language
        await session.execute(query)
        await session.commit()

    @staticmethod
    @with_session
    async def add_crypto_contract(chat_id, contract, session):
        query = (
            update(User)
            .where(User.chat_id == chat_id)
            .values(crypto=User.crypto + ' ' + contract)
        )
        await session.execute(query)
        await session.commit()

    @staticmethod
    @with_session
    async def delete_crypto_contract(chat_id, contract, session):
        query = select(User).where(User.chat_id == chat_id)
        result = await session.execute(query)
        user = result.scalars().first()
        crypto = user.crypto.split()

        if contract not in crypto:
            return False

        crypto.remove(contract)
        result_crypto = ' '.join(crypto)
        user.crypto = result_crypto
        fake_redis[f'user{chat_id}|crypto'] = result_crypto

        await session.execute(query)
        await session.commit()
        return True
