#Veritabanı için kullanılacak modeller burada oluşturulur.

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Enum
from datetime import datetime

from ..database import Base
from .enums import Gender

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    name = Column(String, unique=True)
    hashed_password = Column(String, nullable=False)
    created_dt = Column(DateTime, default=datetime.utcnow())

    #PROFILE
    birthDate = Column(Date)
    gender = Column(Enum(Gender))
    profile_pic = Column(String) #Görselin linkini saklayacak
    biography = Column(String)
    location = Column(String)