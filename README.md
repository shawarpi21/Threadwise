# Threadwise — Verified Memory & Reliability for AI Agents

Threadwise is a Python project built to explore a practical problem with AI agents: **how can an agent remember important information, follow user constraints, and learn from recorded failures without repeating the same mistakes?**

An AI agent may produce a useful answer but still make a decision that goes against a user's requirements. For example, if someone wants a remote job, recommending an onsite-only position is not helpful.

Threadwise provides a simple way to store user goals, check actions against defined rules, record failures, and maintain lessons that pass basic verification checks.

The idea is to make AI agent behaviour more consistent, traceable, and easier to inspect.

## The Problem

AI agents can make mistakes even when the task seems straightforward. Some common problems include:

- Forgetting important user requirements.
- Suggesting actions that violate defined constraints.
- Repeating mistakes that have already been recorded.
- Storing lessons without checking whether the supporting evidence is meaningful.
- Making decisions that are difficult to inspect or explain.

Threadwise explores how structured memory and rule-based checks can help address these problems.

## What Threadwise Does

The project currently includes five main capabilities:

**1. Goal and Constraint Management**

Stores user goals along with constraints that should be considered when evaluating actions. A goal can also specify whether approval is required.

**2. Rule-Based Policy Evaluation**

Checks proposed actions against defined rules and constraints. For example, a job location can be checked against a remote-work preference.

**3. Verified Memory**

Stores lessons with a title, description, and supporting evidence. Lessons must pass basic validation checks before they are marked as verified and returned by the verified-lessons endpoint.

**4. Failure Tracking**

Records failures so they can be reviewed later. This creates a structured record of problems instead of leaving them as untracked events.

**5. Interactive Dashboard**

Provides a visual interface to inspect goals, browse verified lessons, review failure records, search available memories, and check the API's health.

## How It Works

The current workflow is straightforward:

1. A goal and its constraints are submitted to the API.
2. A proposed action is evaluated against the available policy rules.
3. If a failure occurs, it can be recorded for later review.
4. A lesson can be created with a description and supporting evidence.
5. The lesson goes through validation checks before it can be marked as verified.
6. The dashboard provides a convenient way to inspect the stored information.

This separates the storage of information, rule-based decision checks, and review of recorded results.

## Example Use Case

Imagine a user who wants to find a remote AI/ML engineering role.

The user's goal is stored with a constraint such as:

`Do not recommend onsite-only jobs.`

If a proposed job conflicts with the user's location preference, Threadwise's policy checks can identify the violation when the relevant rule and job information are supplied.

The failure can then be recorded, and a related lesson can be created with supporting evidence. Once the lesson passes the current validation checks, it can be marked as verified.

This example illustrates the intended workflow. The current implementation does not automatically discover jobs, independently establish facts, or guarantee that an agent will never repeat a mistake.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | API endpoints and request handling |
| Pydantic | Data validation |
| SQLAlchemy | Database models and database operations |
| SQLite | Local data storage |
| Streamlit | Interactive dashboard |
| Requests | Communication between the dashboard and API |
| Pytest | Automated testing |

## Project Structure

```text
Threadwise/
├── app/
│   ├── core/
│   │   ├── goal.py
│   │   ├── lesson.py
│   │   └── policy.py
│   ├── database/
│   │   └── connection.py
│   ├── models/
│   │   ├── goal_model.py
│   │   ├── lesson_model.py
│   │   └── failure_model.py
│   └── main.py
├── tests/
├── dashboard.py
└── .gitignore
```

The exact contents of individual folders may change as the project develops.

## Getting Started

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Threadwise
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the URL of this repository.

### 2. Create and activate a virtual environment

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install the dependencies

Install the packages used by the project:

```bash
python -m pip install fastapi uvicorn pydantic sqlalchemy pytest python-dotenv streamlit requests pandas httpx
```

### 4. Start the API

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Open the interactive API documentation at:

`http://127.0.0.1:8000/docs`

### 5. Start the dashboard

Open a second terminal in the project folder, activate the virtual environment, and run:

```bash
python -m streamlit run dashboard.py
```

Streamlit will display the local address where the dashboard can be opened in your browser.

### 6. Run the tests

```bash
python -m pytest -v
```

The tests cover important application workflows, including goal handling, policy evaluation, lesson validation, failure recording, and error handling.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check the API's root endpoint |
| GET | `/health` | Check API health |
| POST | `/goals` | Create a goal |
| GET | `/goals` | Retrieve stored goals |
| DELETE | `/goals/{goal_id}` | Delete a goal |
| POST | `/policies/evaluate` | Evaluate an action against policy rules |
| GET | `/lessons` | Retrieve verified lessons |
| POST | `/lessons` | Create a lesson |
| POST | `/lessons/{lesson_id}/verify` | Run lesson verification checks |
| POST | `/failures` | Record a failure |
| GET | `/failures` | Retrieve recorded failures |

## Verification and Reliability

Verification is an important part of this project, but it is important to be precise about what it means.

Threadwise checks lesson fields and supporting evidence using predefined validation rules. These checks include minimum text lengths, a minimum number of distinct evidence words, and a check that the evidence is not identical to the description.

Passing these checks does **not** prove that a lesson is factually correct. The current implementation does not independently verify sources, use a trained machine learning model to judge truth, or automatically learn from failures.

The purpose of the current version is to establish a testable foundation for structured memory and rule-based reliability checks.

## Testing

Automated tests are included to check expected behaviour and catch regressions as the project evolves.

The suite covers core API operations, database-backed workflows, policy checks, lesson verification, and error responses.

Run the test suite locally with:

```bash
python -m pytest -v
```

## Current Limitations and Future Improvements

Threadwise is an ongoing project. The current version focuses on the core components rather than a complete autonomous agent system.

Possible next improvements include:

- Connecting the memory layer to an actual AI agent.
- Retrieving relevant memories based on the current task.
- Adding source-backed evidence verification.
- Connecting recorded failures to a review and improvement workflow.
- Adding more advanced policy rules and configurable approval flows.
- Evaluating whether stored lessons actually reduce repeated errors.
- Adding authentication and stronger controls for production use.

These are planned directions, not claims about features already implemented.

## What I Learned

Building Threadwise has helped me work with API development, data validation, database models, automated testing, and connecting a dashboard to a backend service.

It has also helped me think about an important aspect of AI engineering: producing an answer is only one part of the problem. An agent also needs to respect constraints, maintain useful context, and make its decisions easier to inspect.

I built this project to explore those ideas through a working Python application and to create a foundation that I can extend into a more complete AI agent reliability system.
