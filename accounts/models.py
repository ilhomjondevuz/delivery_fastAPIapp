from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), nullable=False, unique=True)
    email = Column(String(250), nullable=True, unique=True)
    fullname = Column(String(250), nullable=True)
    phone_number = Column(String(250), nullable=True)
    password = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % self.username