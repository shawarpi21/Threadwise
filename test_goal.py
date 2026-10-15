import pytest
from pydantic import ValidationError

from app.core.goal import UserGoal


def test_valid_goal_is_created():
    goal = UserGoal(goal="Find suitable AI jobs")

    assert goal.goal == "Find suitable AI jobs"
    assert goal.constraints == []
    assert goal.approval_required is True


def test_goal_cannot_be_too_short():
    with pytest.raises(ValidationError):
        UserGoal(goal="Job")


def test_constraints_are_preserved():
    goal = UserGoal(
        goal="Find suitable AI jobs",
        constraints=["Do not invent qualifications"],
    )

    assert "Do not invent qualifications" in goal.constraints
