import uuid

from app.services.db.base import Base
from app.constants.database_constants import USER_DB
from sqlalchemy import  ForeignKey
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, create_engine


# engine = create_engine(f"jdbc:mysql://localhost:3307/")
class PromptMaster(Base):
    __tablename__ = 'promptMaster'
    id = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)
    section = Column(String)
    tags = Column(String)
    topic = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    __table_args__ = {"mysql_engine": "InnoDB"}


class Ratings(Base):
    __tablename__ = 'ratings'
    prompt_id = Column(String, ForeignKey('promptMaster.id'), primary_key=True)
    rating = Column(Integer)
    __table_args__ = {"mysql_engine": "InnoDB"}

