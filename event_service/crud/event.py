"""
CRUD layer for Event objects
"""
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


def update_event(db: Session, event: schemas.Event):
    """

    @param db:
    @param event:
    @return:
    """
    stmt = (
        update(models.Event)
        .where(models.Event.id == event.id)
        .values(**event.model_dump(exclude={'id'}))
    )
    db.execute(stmt)
    db.commit()

    # Due to sqlite3 being VERY hard to upgrade (recompile python and override external dependency),
    # we're just going to get the event again instead of using RETURNING function.
    # There are better ways to handle this (checking driver type and changing method), but that will
    # have to wait
    return get_event(db, event.id)


def delete_event(db: Session, event_id: int):
    """

    @param db:
    @param event_id:
    @return:
    """
    stmt = (
        delete(models.Event)
        .where(models.Event.id == event_id)
    )
    db.execute(stmt)
    db.commit()
