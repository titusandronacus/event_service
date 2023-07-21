from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..models import Event, EventCreate
from ..crud import event as event_crud
from ..dependencies import get_db


router = APIRouter(prefix="/events")


@router.get("/", response_model=list[Event])
def read_events(name: str | None = None, db: Session = Depends(get_db)):
    """
    # here be some markdown!
    """
    return event_crud.get_events(db, name)


@router.get("/{event_id}", response_model=Event)
def read_event_by_id(event_id: int, db: Session = Depends(get_db)):
    """
    # here be some markdown!
    """
    db_event = event_crud.get_event(db, event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@router.post("/", response_model=Event)
def create_event(new_event: EventCreate, db: Session = Depends(get_db)):
    """
    # here be some markdown!
    """
    return event_crud.create_event(db, new_event)


# @router.patch("/{event_id}")
# def update_event(event_id: int):
#     # update event via json_patch
#     pass
#
#
# @router.delete("/{event_id}")
# def delete_event(event_id):
#     # delete event by id
#     pass
