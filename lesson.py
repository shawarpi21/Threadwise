
from pydantic import BaseModel, ConfigDict, Field


class Lesson(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=5)
    description: str = Field(min_length=10)
    evidence: str = Field(min_length=10)


class LessonVerification(BaseModel):
    test_passed: bool
