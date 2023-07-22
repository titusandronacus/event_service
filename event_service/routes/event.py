from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..models import Event, EventCreate, EventUpdate
from ..crud import event as event_crud
from ..dependencies import get_db, get_current_user


router = APIRouter(prefix="/events",
                   dependencies=[Depends(get_current_user)]
                   )


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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return db_event


@router.post("/", response_model=Event)
def create_event(new_event: EventCreate, db: Session = Depends(get_db)):
    """
    # here be some markdown!
    """
    return event_crud.create_event(db, new_event)


@router.patch("/{event_id}", response_model=Event)
def update_event(event_id: int, event: EventUpdate, db: Session = Depends(get_db)):
    event_to_update = event_crud.get_event(db, event_id)
    if event_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    event_to_update = Event.model_validate(event_to_update)
    update_data = event.model_dump(exclude_unset=True)
    updated_event = event_crud.update_event(db, event_to_update.model_copy(update=update_data))
    return updated_event



#
# @router.delete("/{event_id}")
# def delete_event(event_id):
#     # delete event by id
#     pass
