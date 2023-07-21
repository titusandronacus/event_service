from fastapi import FastAPI

from .routes.event import router as event_router
from .auth.auth_route import router as auth_router
from .models.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(event_router)
app.include_router(auth_router)
