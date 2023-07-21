from sqlalchemy.orm import Session
from sqlalchemy import update, delete

from ..models import models, schemas


def get_events(db: Session, name: str = None):
    """

    @param db:
    @param name:
    @return:
    """
    q = db.query(models.Event)
    # TODO: why doesn't this filter actually filter stuff?
    # if name is not None:
    #     q.filter_by(name=name)

    return q.all()


def get_event(db: Session, event_id: int):
    """

    @param db:
    @param event_id:
    @return:
    """
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def create_event(db: Session, event: schemas.EventCreate):
    """

    @param db:
    @param event:
    @return:
    """
    db_event = models.Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


# def update_event(db: Session, event: schemas.Event):
#     """
#
#     @param db:
#     @param event:
#     @return:
#     """
#     return db.execute(update(models.Event).where(models.Event.id == event.id).values(event.model_dump()))
#
#
# def delete_event(db: Session, event_id: int):
#     """
#
#     @param db:
#     @param event_id:
#     @return:
#     """
#     return db.execute()