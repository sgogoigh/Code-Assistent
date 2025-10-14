# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(260), nullable=True)
    language = Column(String(50), nullable=True)
    code_excerpt = Column(Text, nullable=True)
    raw_response = Column(Text, nullable=True)
    parsed_report = Column(Text, nullable=True) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())
