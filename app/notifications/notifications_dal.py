from typing import List, Optional, Any
import uuid
from sqlalchemy import update, desc, delete, func
from sqlalchemy.future import select
from .models import Notification, receivers_notifications_association
from sqlalchemy.orm import selectinload
from app.database import get_db, async_session as session
from sqlalchemy import desc
from app.user.models import User
from datetime import datetime, timedelta


class NotificationDAL:
    def __init__(self, db_session: session):
        self.db_session = db_session

    async def get_notifications(self):
        notification = await self.db_session.execute(select(Notification).options(selectinload(Notification.receivers)))
        notification.unique()
        return notification.scalars().all()

    async def get_user_notifications(self, user_id):
        user_obj = await self.get_user(user_id)
        if not user_obj:
            return None
        notification = await self.db_session.execute(
            select(Notification)
            .filter(Notification.receivers.contains(user_obj))\
            .order_by(desc(Notification.created_at)))
        notification.unique()
        return notification.scalars().all()

    async def create_notification(self, notification_type, title, text, user, receivers):
        if user:
            user = user.id
        new_notification = Notification(
            notification_type=notification_type,
            title=title,
            text=text,
            user_id=user,
            receivers=receivers
        )
        self.db_session.add(new_notification)
        return new_notification

    async def update_notification(
        self,
        notification_id,
        notification_type: Optional[str] is None,
        title: Optional[str] is None,
        text: Optional[str] is None,
    ):
        q = update(Notification).filter(Notification.id == notification_id)
        if notification_type:
            q = q.values(notification_type=notification_type)
        if text:
            q = q.values(text=text)
        if title:
            q = q.values(title=title)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)
        return 'Обновлено'

    async def delete_notification(self, notification_id):
        stmt = delete(Notification).filter(Notification.id == notification_id)
        await self.db_session.execute(stmt)

    async def get_user(self, user_id):
        user = await self.db_session.execute(select(User).filter(User.id == user_id))
        return user.scalars().first()

    async def get_receievers(self, receivers):
        receivers_list = [(await self.db_session.execute(select(User).filter(User.id == user)))
                          .scalars().first() for user in receivers if (await self.db_session.execute(select(User).filter(User.id == user)))
                          .scalars().first() is not None]
        return receivers_list

    async def get_receievers_tokens(self, receivers):
        receivers_list = [(await self.db_session.execute(select(User.token).filter(User.id == user)))
                          .scalars().first() for user in receivers if (await self.db_session.execute(select(User).filter(User.id == user)))
                          .scalars().first() is not None]
        return receivers_list

    async def delete_expired_notifications(self):
        time_30_days_ago = datetime.now() - timedelta(days=30)
        stmt = delete(Notification).filter(Notification.created_at < time_30_days_ago)
        await self.db_session.execute(stmt)
        print('Удалены уведомления сроком более 30 дней')
        return 'Удалены уведомления сроком более 30 дней'

    async def get_all_receivers(self):
        user = await self.db_session.execute(select(User.token))
        return user.scalars().all()
