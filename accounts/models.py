from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(250), nullable=False, unique=True)
    email = Column(String(250), unique=True)
    fullname = Column(String(250), nullable=True)
    phone_number = Column(String(250), nullable=True)
    password = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)

    orders = relationship(
        "Order",
        back_populates="user",
    )

    def __repr__(self):
        return '<User %r>' % self.username