from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from typing import Optional

from . import schemas
from . import logic
from .m_utils import get_current_user


router = APIRouter(
    prefix='/event'
)

router_m = APIRouter(
    prefix='/events'
)


def HTTPanswer(status_code, description):
    return JSONResponse(
        status_code=status_code,
        content={'content': description},
    )


# external routes for manage events

@router.post('/create')
async def create_event(event: schemas.CreateEvent,
                       current_user = Depends(get_current_user)):
    event_id = await logic.create_event(current_user.account_id, event)
    return HTTPanswer(201, event_id)


@router_m.get('/all')
async def get_all_events(offset: Optional[int] = Query(None), limit: Optional[int] = Query(None)):
    return await logic.get_all_events(offset, limit)


@router.get('/{event_id}')
async def get_event_info(event_id: int):
    return await logic.get_event_info(event_id)


@router.get('/{event_id}/join')
async def join_event(event_id: int,
                     current_user = Depends(get_current_user)):
    await logic.join_event(current_user.account_id, event_id)
    return HTTPanswer(200, 'Entered')


@router.get('/{event_id}/leave')
async def leave_event(event_id: int,
                      current_user = Depends(get_current_user)):
    await logic.leave_event(current_user.account_id, event_id)
    return HTTPanswer(200, 'Leaved')
