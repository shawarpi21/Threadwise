

import pytest
from pydantic import ValidationError

from app.core.lesson import Lesson


def test_lesson_is_created_with_valid_data():
    lesson = Lesson(
        title="Check job location",
        description="Compare job location with user preferences.",
        evidence="An onsite-only job conflicted with the remote preference.",
    )

    assert lesson.title == "Check job location"
    assert lesson.description == (
        "Compare job location with user preferences."
    )


def test_lesson_rejects_short_title():
    with pytest.raises(ValidationError):
        Lesson(
            title="Bad",
            description="Compare job location with user preferences.",
            evidence="An onsite-only job conflicted with the remote preference.",
        )


def test_lesson_rejects_verified_field():
    with pytest.raises(ValidationError):
        Lesson(
            title="Check job location",
            description="Compare job location with user preferences.",
            evidence="An onsite-only job conflicted with the remote preference.",
            verified=True,
        )
