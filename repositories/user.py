from typing import List
from sqlalchemy import select, update, delete

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
            tasks = [user_model for user_model in users_models]
            return tasks

    @classmethod
    async def get_user_by_id(cls, user_id: int):
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.id == user_id)
            result = await session.execute(query)
            task = result.scalars().first()
            return task

    @classmethod
    async def get_user_by_tg_id(cls, user_tg_id: str) -> UserOrm:
        async with new_session() as session:
            query = select(UserOrm).where(UserOrm.tg_id == user_tg_id)
            result = await session.execute(query)
            user = result.scalars().first()
            return user