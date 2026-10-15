
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.connection import Base
from app.core.lesson_model import LessonRecord


def create_test_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    TestSession = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    return engine, TestSession()


def test_save_and_retrieve_lesson():
    engine, session = create_test_session()

    try:
        lesson = LessonRecord(
            title="Check job location",
            description="Compare job location with user preferences.",
            evidence="A test showed an onsite-only job violated the remote preference.",
        )

        session.add(lesson)
        session.commit()

        saved_lesson = (
            session.query(LessonRecord)
            .filter_by(title="Check job location")
            .first()
        )

        assert saved_lesson is not None
        assert saved_lesson.description == (
            "Compare job location with user preferences."
        )
        assert saved_lesson.verified is False
    finally:
        session.close()
        engine.dispose()


def test_delete_lesson():
    engine, session = create_test_session()

    try:
        lesson = LessonRecord(
            title="Check job location",
            description="Compare job location with user preferences.",
            evidence="A test showed an onsite-only job violated the remote preference.",
        )

        session.add(lesson)
        session.commit()

        session.delete(lesson)
        session.commit()

        remaining = session.query(LessonRecord).all()
        assert remaining == []
    finally:
        session.close()
        engine.dispose()
