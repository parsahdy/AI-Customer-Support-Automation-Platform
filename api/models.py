from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime, UTC


class QA(Base):
    __tablename__ = "qa"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now(UTC))