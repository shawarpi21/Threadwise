from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.connection import Base
from app.core.goal_model import GoalRecord


def create_test_database():
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

    return TestSession


def test_goal_can_be_saved_and_retrieved():
    TestSession = create_test_database()
    db = TestSession()

    try:
        goal = GoalRecord(
            goal="Learn machine learning",
            constraints=["Use practical examples"],
            approval_required=True,
        )

        db.add(goal)
        db.commit()

        saved_goal = db.query(GoalRecord).first()

        assert saved_goal is not None
        assert saved_goal.goal == "Learn machine learning"
        assert saved_goal.constraints == ["Use practical examples"]
        assert saved_goal.approval_required is True
    finally:
        db.close()


def test_goal_can_be_deleted():
    TestSession = create_test_database()
    db = TestSession()

    try:
        goal = GoalRecord(
            goal="Practice Python",
            constraints=[],
            approval_required=True,
        )

        db.add(goal)
        db.commit()
        goal_id = goal.id

        db.delete(goal)
        db.commit()

        deleted_goal = db.query(GoalRecord).filter_by(id=goal_id).first()

        assert deleted_goal is None
    finally:
        db.close()