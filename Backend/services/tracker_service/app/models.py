# SQLAlcemy ORM tables definitions

from sqlalchemy import Column, Integer, String, Float, DataTime
from datetime import datetime
from .database import Base

class ExamCountdownModel(Base):
    __tablename__ = "exam_countdowns"

    id = Column(Integer, primary_key=True, index=True, autoincrememt=True)
    subject = Column(String, index=True, nullable=False)
    exam_date = Column(DateTime, nullable=False)
    target_hours = Column(Float, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow)