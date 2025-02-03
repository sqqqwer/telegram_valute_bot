from database.database import session_factory


def with_session(method):
    async def wrapper(*args, **kwargs):
        async with session_factory() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as exception:
                await session.rollback()
                raise exception
            finally:
                await session.close()
    return wrapper
