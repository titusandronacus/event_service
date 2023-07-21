import os

os.environ['DATABASE_URL'] = "sqlite:///./tests/test.db"

def pytest_sessionfinish(session, exitstatus):
    os.remove("./tests/test.db")
