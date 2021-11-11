from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    ForeignKey,
    Table,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.user.models import User

from app.database import Base

receivers_notifications_association = Table(
    'recievers_notifications',
    Base.metadata,
    Column('Notification_id', Integer, ForeignKey('Notifications.id', ondelete="CASCADE")),
    Column('User_id', String, ForeignKey('Users.id', ondelete="CASCADE")),
)


class Notification(Base):
    __tablename__ = 'Notifications'
    id = Column(Integer, primary_key=True, index=True)
    notification_type = Column(String, nullable=False)
    title = Column(String(50))
    text = Column(Text)
    user_id = Column(String, ForeignKey("Users.id"), nullable=True)
    receivers = relationship(
        'User', secondary=receivers_notifications_association,
        backref='notifications_to_receive'
    )
    created_at = Column(
        DateTime(timezone=True), nullable=True, server_default=func.now()
    )
