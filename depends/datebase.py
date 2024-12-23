from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

import models

engine = create_async_engine("sqlite+aiosqlite:///users.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

async def create_tables():
   async with engine.begin() as conn:
      await conn.run_sync(models.UserOrm.metadata.create_all)


async def delete_tables():
   async with engine.begin() as conn:
      await conn.run_sync(models.UserOrm.metadata.drop_all)