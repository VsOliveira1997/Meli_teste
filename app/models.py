from sqlalchemy import Column, Integer, String
from app.database import Base

class ExcludedIP(Base):
    __tablename__ = "excluded_ips"
    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, unique=True, index=True)