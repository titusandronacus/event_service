"""
Contains application dependencies for Event Service
"""
from .models.database import SessionLocal
from .auth.app_dependencies import get_current_user, oauth2_scheme


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



