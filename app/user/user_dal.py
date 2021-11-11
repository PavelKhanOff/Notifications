from typing import List, Optional
import uuid
from sqlalchemy import update, desc, delete, func
from sqlalchemy.future import select
from .models import User
from app.database import get_db, async_session as session


class UserDAL:
    def __init__(self, db_session: session):
        self.db_session = db_session

    async def get_user(self, user_id):
        user = await self.db_session.execute(select(User).filter(User.id == user_id))
        return user.scalars().first()

    async def get_users(self):
        user = await self.db_session.execute(select(User))
        return user.scalars().all()

    async def create_user(
        self,
        id,
        token,
        username

    ):
        new_user = User(
            id=id,
            token=token,
            username=username
        )
        self.db_session.add(new_user)
        return new_user

    async def update_user(
        self,
        user_id,
        id: Optional[int] is None,
        token: Optional[str] is None,
        username: Optional[str] is None
    ):
        q = update(User).filter(User.id == user_id)
        if id:
            q = q.values(id=id)
        if token:
            q = q.values(token=token)
        if username:
            q = q.values(username=username)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)
        return 'Обновлено'

    async def delete_user(self, user_id):
        stmt = delete(User).where(User.id == user_id)
        await self.db_session.execute(stmt)
