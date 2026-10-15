
from sqlalchemy import Boolean, Column, Integer, String
from app.database.connection import Base


class LessonRecord(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    evidence = Column(String, nullable=False)
    verified = Column(Boolean, nullable=False, default=False)
