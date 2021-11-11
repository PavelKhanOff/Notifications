from app.database import async_session
from .notifications_dal import NotificationDAL


async def get_notification_dal():
    async with async_session() as session:
        async with session.begin():
            yield NotificationDAL(session)
