from fastapi import APIRouter, Depends, status
from .notifications_dal import NotificationDAL
from app.notifications import schemas
from .dependencies import get_notification_dal
from fastapi_pagination.paginator import paginate as paginate_list
from app.pagination import CustomPage as Page
from fastapi.responses import JSONResponse
from app.sender.tasks import send_notification
from app.auth.jwt_decoder import get_superuser
from http import HTTPStatus
from starlette.responses import Response


router = APIRouter(tags=['Notifications'])


@router.get('/notifications', response_model=Page[schemas.NotificationOut], dependencies=[Depends(get_superuser)])
async def get_notifications(
        notification_dal: NotificationDAL = Depends(get_notification_dal)
):
    notifications = await notification_dal.get_notifications()
    return paginate_list(notifications)


@router.get('/notifications/get_user/{user_id}', response_model=Page[schemas.NotificationUserOut], dependencies=[Depends(get_superuser)])
async def get_user_notifications(
        user_id: str,
        notification_dal: NotificationDAL = Depends(get_notification_dal)
):
    notifications = await notification_dal.get_user_notifications(user_id)
    if not notifications:
        return JSONResponse(status_code=403, content="Пользователя не существует")
    return paginate_list(notifications)


@router.post('/notifications/create', status_code=201, dependencies=[Depends(get_superuser)])
async def create_notification(
        request: schemas.CreateNotification,
        notification_dal: NotificationDAL = Depends(get_notification_dal)
):
    user_obj = await notification_dal.get_user(request.user_id)
    receivers = await notification_dal.get_receievers(request.receivers)
    if len(receivers) == 0 or receivers is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content='Подписчиков нет')
    notification = await notification_dal.create_notification(
        request.notification_type,
        request.title,
        request.text,
        user_obj,
        receivers)
    receivers = [user.token for user in notification.receivers]
    await send_notification.delay(notification.title, notification.text, receivers)
    return notification


@router.patch('/notifications/{notification_id}/update', status_code=202, dependencies=[Depends(get_superuser)])
async def update_notification(
        notification_id: int,
        request: schemas.UpdateNotification,
        notification_dal: NotificationDAL = Depends(get_notification_dal)
):
    notification = await notification_dal.update_notification(
        notification_id,
        request.notification_type,
        request.title,
        request.text)
    return notification


@router.delete('/notifications/{notification_id}/delete', status_code=HTTPStatus.NO_CONTENT, dependencies=[Depends(get_superuser)])
async def delete_notification(
        notification_id: int,
        notification_dal: NotificationDAL = Depends(get_notification_dal)
):
    await notification_dal.delete_notification(notification_id)
    return Response(status_code=204)


@router.post('/notifications/send_custom_notifications', status_code=200, dependencies=[Depends(get_superuser)])
async def send_custom_notifications(
        request: schemas.CustomNotifications,
        notification_dal: NotificationDAL = Depends(get_notification_dal)
):
    receivers = request.receivers
    if receivers == ['all']:
        receivers = await notification_dal.get_all_receivers()
        await send_notification.delay(request.title, request.text, receivers)
        return 'send'
    receivers = await notification_dal.get_receievers_tokens(request.receivers)
    if len(receivers) == 0 or receivers is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content='Подписчиков нет')
    await send_notification.delay(request.title, request.text, receivers)
    return 'send'
