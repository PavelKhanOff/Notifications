from app.FCM import FCMmanager
from app.celery.app import celery_app
from fastapi import APIRouter
from app.notifications.notifications_dal import NotificationDAL
from app.database import async_session
from celery.schedules import crontab

router = APIRouter(tags=['Notifications'])


@celery_app.task
async def send_notification(title, msg, tokens):
    res = FCMmanager.sendpush(
        title=title,
        msg=msg,
        registration_tokens=tokens)
    return res


@celery_app.on_after_finalize.connect
async def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=0, minute=0),
        delete_notifications.s(),
        name='delete expired notifications')


@celery_app.task
async def delete_notifications():
    async with async_session() as session:
        async with session.begin():
            dal = NotificationDAL(session)
            return await dal.delete_expired_notifications()
