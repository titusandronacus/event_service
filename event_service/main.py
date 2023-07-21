from fastapi import FastAPI

from .routes.event import router as event_router
from .models.database import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(event_router)
