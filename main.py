from app.core.failure_model import FailureRecord
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.goal import UserGoal
from app.core.goal_model import GoalRecord
from app.core.lesson import Lesson
from app.core.lesson_model import LessonRecord
from app.core.policy import (
    evaluate_action,
    check_constraint_violations,
    check_job_location_constraints,
)
from app.database.connection import Base, engine, SessionLocal


app = FastAPI(
    title="Threadwise",
    description="A reliability system for AI agents",
    version="0.1.0",
)

Base.metadata.create_all(bind=engine)


class PolicyRequest(BaseModel):
    goal: str
    action_description: str
    constraints: list[str] = Field(default_factory=list)
    approval_required: bool = True
    user_approved: bool = False


@app.get("/")
def home():
    return {
        "project": "Threadwise",
        "message": "Our AI reliability journey starts here!",
        "status": "running",
    }


@app.post("/goals")
def create_goal(goal: UserGoal):
    db: Session = SessionLocal()

    try:
        new_goal = GoalRecord(
            goal=goal.goal,
            constraints=goal.constraints,
            approval_required=goal.approval_required,
        )

        db.add(new_goal)
        db.commit()
        db.refresh(new_goal)

        return {
            "message": "Goal saved successfully",
            "id": new_goal.id,
            "goal": goal.model_dump(),
        }
    finally:
        db.close()


@app.get("/goals")
def get_goals():
    db: Session = SessionLocal()

    try:
        goals = db.query(GoalRecord).all()

        return [
            {
                "id": item.id,
                "goal": item.goal,
                "constraints": item.constraints,
                "approval_required": item.approval_required,
            }
            for item in goals
        ]
    finally:
        db.close()


@app.delete("/goals/{goal_id}")
def delete_goal(goal_id: int):
    db: Session = SessionLocal()

    try:
        goal_record = (
            db.query(GoalRecord)
            .filter(GoalRecord.id == goal_id)
            .first()
        )

        if goal_record is None:
            raise HTTPException(
                status_code=404,
                detail="Goal not found",
            )

        db.delete(goal_record)
        db.commit()

        return {
            "message": "Goal deleted successfully",
            "id": goal_id,
        }
    finally:
        db.close()


@app.post("/policies/evaluate")
def evaluate_policy(request: PolicyRequest):
    goal = UserGoal(
        goal=request.goal,
        constraints=request.constraints,
        approval_required=request.approval_required,
    )

    violations = check_constraint_violations(
        constraints=goal.constraints,
        action_description=request.action_description,
    )

    location_violations = check_job_location_constraints(
        constraints=goal.constraints,
        action_description=request.action_description,
    )

    violations.extend(location_violations)

    decision = evaluate_action(
        goal=goal,
        action_description=request.action_description,
        user_approved=request.user_approved,
    )

    if violations:
        return {
            "allowed": False,
            "requires_approval": decision.requires_approval,
            "violations": violations,
            "reason": "Action may violate a user constraint.",
        }

    return {
        "allowed": decision.allowed,
        "requires_approval": decision.requires_approval,
        "violations": [],
        "reason": decision.reason,
    }


@app.get("/lessons")
def get_lessons():
    db: Session = SessionLocal()

    try:
        lessons = (
            db.query(LessonRecord)
            .filter(LessonRecord.verified.is_(True))
            .all()
        )

        return [
            {
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "evidence": item.evidence,
                "verified": item.verified,
            }
            for item in lessons
        ]
    finally:
        db.close()


@app.post("/lessons")
def create_lesson(lesson: Lesson):
    db: Session = SessionLocal()

    try:
        new_lesson = LessonRecord(
            title=lesson.title,
            description=lesson.description,
            evidence=lesson.evidence,
        )

        db.add(new_lesson)
        db.commit()
        db.refresh(new_lesson)

        return {
            "message": "Lesson saved successfully",
            "id": new_lesson.id,
            "title": new_lesson.title,
            "description": new_lesson.description,
            "evidence": new_lesson.evidence,
            "verified": new_lesson.verified,
        }
    finally:
        db.close()


@app.post("/lessons/{lesson_id}/verify")
def verify_lesson(lesson_id: int):
    db: Session = SessionLocal()

    try:
        lesson = (
            db.query(LessonRecord)
            .filter(LessonRecord.id == lesson_id)
            .first()
        )

        if lesson is None:
            raise HTTPException(
                status_code=404,
                detail="Lesson not found",
            )

        title = lesson.title.strip()
        description = lesson.description.strip()
        evidence = lesson.evidence.strip()

        if len(title) < 5:
            raise HTTPException(
                status_code=400,
                detail="Lesson title is too short.",
            )

        if len(description) < 10:
            raise HTTPException(
                status_code=400,
                detail="Lesson description is too short.",
            )

        if len(evidence) < 20:
            raise HTTPException(
                status_code=400,
                detail="Evidence must contain at least 20 characters.",
            )

        if len(set(evidence.split())) < 4:
            raise HTTPException(
                status_code=400,
                detail="Evidence must contain at least 4 distinct words.",
            )

        if evidence.casefold() == description.casefold():
            raise HTTPException(
                status_code=400,
                detail="Evidence must be different from the lesson description.",
            )

        lesson.verified = True
        db.commit()
        db.refresh(lesson)

        return {
            "message": "Lesson passed the content-quality checks.",
            "id": lesson.id,
            "verified": lesson.verified,
            "checks": {
                "title_length": True,
                "description_length": True,
                "evidence_length": True,
                "evidence_word_variety": True,
                "evidence_differs_from_description": True,
            },
        }

    finally:
        db.close()


class FailureCreate(BaseModel):
    action_description: str = Field(min_length=5)
    failure_reason: str = Field(min_length=10)
    expected_behavior: str = Field(min_length=10)


@app.post("/failures")
def create_failure(failure: FailureCreate):
    db: Session = SessionLocal()

    try:
        record = FailureRecord(
            action_description=failure.action_description,
            failure_reason=failure.failure_reason,
            expected_behavior=failure.expected_behavior,
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "message": "Failure recorded successfully",
            "id": record.id,
            "action_description": record.action_description,
            "failure_reason": record.failure_reason,
            "expected_behavior": record.expected_behavior,
        }
    finally:
        db.close()

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": "Threadwise",
    }


@app.get("/failures")
def get_failures():
    db: Session = SessionLocal()

    try:
        failures = db.query(FailureRecord).all()

        return [
            {
                "id": item.id,
                "action_description": item.action_description,
                "failure_reason": item.failure_reason,
                "expected_behavior": item.expected_behavior,
            }
            for item in failures
        ]
    finally:
        db.close()
