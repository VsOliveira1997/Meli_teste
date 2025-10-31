from sqlalchemy import Column, Integer, String
from app.database import Base

class ExcludedIP(Base):
    __tablename__ = "excluded_ips"
    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, unique=True, index=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)