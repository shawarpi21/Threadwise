
from sqlalchemy import Column, Integer, String, Text
from app.database.connection import Base


class FailureRecord(Base):
    __tablename__ = "failures"

    id = Column(Integer, primary_key=True, index=True)
    action_description = Column(String, nullable=False)
    failure_reason = Column(Text, nullable=False)
    expected_behavior = Column(Text, nullable=False)
