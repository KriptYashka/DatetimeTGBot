from typing import List
from sqlalchemy import select, update, delete, CursorResult

from depends.datebase import new_session
from models.user import UserOrm


class UserRepository:
    @classmethod
    async def create_user(cls, user: UserOrm) -> UserOrm:
        async with new_session() as session:
            session.add(user)
            await session.flush()
            await session.commit()
            return user

    @classmethod
    async def get_users(cls) -> list[UserOrm]:
        async with new_session() as session:
            query = select(UserOrm)
            result = await session.execute(query)
            users_models = result.scalars().all()
            users = [user_model for user_model in users_models]
            return users

    @classmethod
    async def get_staff_users(cls) -> list[UserOrm]:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.is_staff)
            result = await session.execute(query)
            users_models = result.scalars().all()
            users = [user_model for user_model in users_models]
            return users

    @classmethod
    async def get_user_by_id(cls, user_id: int) -> UserOrm:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.id == user_id)
            result = await session.execute(query)
            user = result.scalars().first()
            return user

    @classmethod
    async def get_user_by_tg_id(cls, user_tg_id: str) -> UserOrm:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.tg_id == user_tg_id)
            result = await session.execute(query)
            user = result.scalars().first()
            return user

    @classmethod
    async def delete_user_by_tg_id(cls, user_tg_id: str):
        async with new_session() as session:
            query = delete(UserOrm).where(UserOrm.tg_id == user_tg_id)
            result: CursorResult = await session.execute(query)
            await session.commit()
            print(query)
            return result