from dataclasses import dataclass

from app.core.goal import UserGoal


@dataclass
class PolicyDecision:
    allowed: bool
    requires_approval: bool
    reason: str


def evaluate_action(
    goal: UserGoal,
    action_description: str,
    user_approved: bool = False,
) -> PolicyDecision:
    """Decide whether a proposed action needs user approval."""

    if not action_description.strip():
        return PolicyDecision(
            allowed=False,
            requires_approval=False,
            reason="Action description cannot be empty.",
        )

    if goal.approval_required and not user_approved:
        return PolicyDecision(
            allowed=False,
            requires_approval=True,
            reason="User approval is required before this action.",
        )

    return PolicyDecision(
        allowed=True,
        requires_approval=False,
        reason="Action passed the current approval policy.",
    )

def check_constraint_violations(
    constraints: list[str],
    action_description: str,
) -> list[str]:
    """Detect simple, explicitly supported constraint violations."""

    violations = []

    action = action_description.casefold()

    for constraint in constraints:
        rule = constraint.casefold()

        if (
            "do not invent qualifications" in rule
            and any(
                phrase in action
                for phrase in [
                    "invent qualification",
                    "fake qualification",
                    "add unearned qualification",
                    "fabricate qualification",
                ]
            )
        ):
            violations.append(
                "Action may violate the constraint: "
                + constraint
            )

    return violations
def check_job_location_constraints(
    constraints: list[str],
    action_description: str,
) -> list[str]:
    """Check a specific, supported job-location constraint."""

    violations = []
    action = action_description.casefold()

    for constraint in constraints:
        rule = constraint.casefold()

        prioritizes_remote = (
            "prioritize remote positions" in rule
            or "prioritise remote positions" in rule
        )

        explicitly_onsite = (
            "onsite-only" in action
            or "on-site only" in action
            or "onsite only" in action
        )

        if prioritizes_remote and explicitly_onsite:
            violations.append(
                "Action may conflict with the constraint: "
                + constraint
            )

    return violations
