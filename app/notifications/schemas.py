import datetime

from pydantic import BaseModel
from typing import List, Any, Union, Optional
from app.user.schemas import UserOut


class NotificationOut(BaseModel):
    id: int
    notification_type: str
    title: str
    text: str
    sender_user: Any
    receivers: List
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class NotificationUserOut(BaseModel):
    id: int
    notification_type: str
    title: str
    text: str
    sender_user: Any
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class CreateNotification(BaseModel):
    notification_type: str
    title: str
    text: str
    user_id: str
    receivers: List

    class Config:
        orm_mode = True


class UpdateNotification(BaseModel):
    notification_type: Optional[str] = None
    title: Optional[str] = None
    text: Optional[str] = None
    user_id: Optional[str] = None

    class Config:
        orm_mode = True


class CustomNotifications(BaseModel):
    title: str
    text: str
    receivers: List
