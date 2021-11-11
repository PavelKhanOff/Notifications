from sqlalchemy import (
    Column,
    String
)
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = 'Users'
    id = Column(String, primary_key=True, index=True)
    token = Column(String, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    notification_to_send = relationship('Notification', backref='sender_user')
