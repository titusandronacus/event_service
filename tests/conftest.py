import os

os.environ['DATABASE_URL'] = "sqlite:///./tests/test.db"
os.environ['ADMIN_USER'] = "tester"
os.environ['ADMIN_PASS'] = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'] = '2'
os.environ['SECRET_KEY'] = "4442f35b79af38642d676b38f06729b5b923f7da882e26e57a06f6123b937fe2"
os.environ['ALGORITHM'] = "HS256"


def pytest_sessionfinish(session, exitstatus):
    os.remove("./tests/test.db")
