from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    name: str


class EventCreate(EventBase):
    pass


class Event(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
