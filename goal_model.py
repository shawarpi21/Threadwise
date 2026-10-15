from sqlalchemy import Boolean, Column, Integer, JSON, String

from app.database.connection import Base


class GoalRecord(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    goal = Column(String, nullable=False)
    constraints = Column(JSON, nullable=False, default=list)
    approval_required = Column(Boolean, nullable=False, default=True)

