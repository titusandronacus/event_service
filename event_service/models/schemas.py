from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    name: str


class EventCreate(EventBase):
    pass


class Event(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class EventUpdate(Event):
    name: str = None
    id: int = None


class BaseUser(BaseModel):
    username: str


class User(BaseUser):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
