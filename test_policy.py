from app.core.policy import check_constraint_violations
from app.core.goal import UserGoal
from app.core.policy import evaluate_action


def test_action_requires_approval_when_configured():
    goal = UserGoal(
        goal="Find suitable AI jobs",
        approval_required=True,
    )

    decision = evaluate_action(
        goal,
        "Submit a job application",
    )

    assert decision.allowed is False
    assert decision.requires_approval is True


def test_action_can_pass_after_approval():
    goal = UserGoal(
        goal="Find suitable AI jobs",
        approval_required=True,
    )

    decision = evaluate_action(
        goal,
        "Submit a job application",
        user_approved=True,
    )

    assert decision.allowed is True
    assert decision.requires_approval is False


def test_empty_action_is_rejected():
    goal = UserGoal(goal="Find suitable AI jobs")

    decision = evaluate_action(goal, "   ")

    assert decision.allowed is False
    assert decision.requires_approval is False

def test_flags_invented_qualifications():
    violations = check_constraint_violations(
        ["Do not invent qualifications"],
        "Invent qualifications on my resume",
    )

    assert len(violations) == 1


def test_allows_unrelated_action_under_this_rule():
    violations = check_constraint_violations(
        ["Do not invent qualifications"],
        "Search for remote AI jobs",
    )

    assert violations == []


def test_does_not_claim_to_detect_every_violation():
    violations = check_constraint_violations(
        ["Do not invent qualifications"],
        "Update my resume",
    )

    assert violations == []

def test_constraint_violation_blocks_action_even_if_approved():
    violations = check_constraint_violations(
        ["Do not invent qualifications"],
        "Invent qualifications on my resume",
    )

    assert violations
    # Approval alone must not override a detected violation.


def test_approval_is_still_required_for_safe_action():
    goal = UserGoal(
        goal="Find suitable AI jobs",
        constraints=["Do not invent qualifications"],
        approval_required=True,
    )

    violations = check_constraint_violations(
        goal.constraints,
        "Search for remote AI jobs",
    )

    decision = evaluate_action(
        goal=goal,
        action_description="Search for remote AI jobs",
        user_approved=False,
    )

    assert violations == []
    assert decision.allowed is False
    assert decision.requires_approval is True

from app.core.policy import check_job_location_constraints

def test_flags_onsite_only_job_when_remote_is_prioritized():
    violations = check_job_location_constraints(
        ["Prioritize remote positions"],
        "Apply to this onsite-only job",
    )

    assert len(violations) == 1


def test_remote_preference_does_not_block_remote_jobs():
    violations = check_job_location_constraints(
        ["Prioritize remote positions"],
        "Search for remote AI jobs",
    )

    assert violations == []
