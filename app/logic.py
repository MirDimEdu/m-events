import uuid
import httpx
from fastapi import Request
from datetime import datetime, timedelta

from .db import events, participations
from .db import _database
from .config import cfg
from . import schemas # maybe fix to from .schemas import CurrenUser
from .errors import HTTPabort


async def create_event(account_id, event):
    query = events.insert().values(account_id=account_id, title=event.title,
                                  description=event.description,
                                  location=event.location,
                                  event_date=datetime.fromisoformat(event.event_date),
                                  created=datetime.utcnow())
    event_id = await _database.execute(query)

    query = participations.insert().values(even=event_id, account_id=account_id,
                                           status='creator')
    await _database.execute(query)
    return event_id


async def get_all_events(offset, limit):
    query = select(events).order_by(desc(events.c.event_date))
    if offset and limit:
        if offset < 0 or limit < 1:
            HTTPabort(422, 'Offset or limit has wrong values')
        else:
            query = query.limit(limit).offset(offset)

    return await _database.fetch_all(query)


async def get_event_info(event_id):
    query = select(events).where(events.c.id == event_id)
    
    event = await _database.fetch_one(query)
    if not event:
        HTTPabort(404, 'Event not found')
    return event


async def join_event(account_id, event_id):
    query = select(events).where(events.c.id == event_id)
    event = await _database.fetch_one(query)
    if not event:
        HTTPabort(404, 'Event not found')

    query = select(participations).where(participations.c.account_id == account_id and
                                         participations.c.event_id == event_id)
    participation = await _database.fetch_one(query)
    if participation:
        HTTPabort(409, 'Already joined')

    query = participations.insert().values(even=event_id, account_id=account_id,
                                           status='visitor')
    await _database.execute(query)


async def leave_event(account_id, event_id):
    query = select(events).where(events.c.id == event_id)
    event = await _database.fetch_one(query)
    if not event:
        HTTPabort(404, 'Event not found')

    query = select(participations).where(participations.c.account_id == account_id and
                                         participations.c.event_id == event_id and
                                         participations.c.status == 'visitor')
    participation = await _database.fetch_one(query)
    if participation:
        query = participations.delete().where(participations.c.account_id == account_id and
                                              participations.c.event_id == event_id)
        await _database.execute(query)
