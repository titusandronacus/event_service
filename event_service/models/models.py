from sqlalchemy import Column, String, Integer

from .database import Base


class Event(Base):
    __tablename__ = 'Events'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
