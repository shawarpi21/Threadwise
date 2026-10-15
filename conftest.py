import os
import tempfile

import pytest


@pytest.fixture(scope="session", autouse=True)
def test_database():
    # Create a separate temporary SQLite database for the test run.
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

    yield

    os.environ.pop("DATABASE_URL", None)

    if os.path.exists(db_path):
        os.remove(db_path)
