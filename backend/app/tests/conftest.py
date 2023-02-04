from api.models import Base
from tests.sample_db import engine, DATABASE_URL

import os


def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    try:
        os.remove(DATABASE_URL)
    except OSError:
        pass

    Base.metadata.create_all(bind=engine)


def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    try:
        os.remove(DATABASE_URL)
    except OSError:
        pass
