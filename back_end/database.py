from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text


class WebDB:

    def __init__(self):
        # Создаем асинхронный движок
        self.engine = create_async_engine("sqlite+aiosqlite:///arbuz.db")
        self.new_session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def user_exists(self, login):
        # Асинхронно открываем сессию
        async with self.new_session() as session:
            command = text("SELECT `login` FROM `users` WHERE `login`=:login")
            result = await session.execute(command, {"login": login})
            user = result.fetchone()
            if user is None:
                return False
            return True

    async def add_user(self, login, password, language):
        async with self.new_session() as session:
            command = text(
                "INSERT INTO `users` (`login`, `password`, `language`) "
                "VALUES(:login, :password, :language)"
            )
            await session.execute(command, {"login": login, "password": password, "language": language})
            await session.commit()

    async def get_user(self, login):
        async with self.new_session() as session:
            command = text(
                "SELECT `id`, `password`, `language`, `info` FROM `users` WHERE `login`=:login"
            )
            result = await session.execute(command, {"login": login})
            return result

    async def close(self):
        await self.engine.dispose()



