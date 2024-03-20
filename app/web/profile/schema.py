import uuid

from app.services.db.base import Base
from app.constants.database_constants import USER_DB
from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, create_engine

# engine = create_engine(f"jdbc:mysql://localhost:3307/")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    about = Column(String)
    is_public = Column(Boolean)
    __table_args__ = {"mysql_engine" : "InnoDB"}
