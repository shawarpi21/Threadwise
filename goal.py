from pydantic import BaseModel, Field


class UserGoal(BaseModel):
    goal: str = Field(min_length=5)
    constraints: list[str] = Field(default_factory=list)
    approval_required: bool = True
