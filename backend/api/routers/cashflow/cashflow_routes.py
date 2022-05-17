import logging
from uuid import uuid4

from fastapi import APIRouter, HTTPException

import api.routers.cashflow.cashflow_schemas as schemas
import api.routers.cashflow.cashflow_formulas as formulas

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
cashflow = APIRouter(tags=["cashflow"])

CACHE = {}
LIMIT = 12


@cashflow.post("/calc-schedule")
def calc_amortization_schedule(schedule_input: schemas.AmortizationScheduleInput):
    amortization = formulas.Amortization.from_schedule_input(schedule_input)
    schedules = amortization.get_monthly_schedule_output()
    uuid = f'{uuid4()}'[:16]
    CACHE[uuid] = schedules
    schedules = schemas.AmortizationSchedule(
        uuid=uuid,
        schedules=schedules[:LIMIT],
        next_offset=LIMIT,
        prev_offset=0,
        total=len(schedules)
    )
    return schedules


@cashflow.get("/schedule")
def get_amortization_schedule(uuid: str, offset: int = 0, limit: int = LIMIT):
    schedules = CACHE.get(uuid)
    if not schedules:
        raise HTTPException(status_code=404, detail={'message': 'not found'})

    prev_offset = offset - limit
    next_offset = offset + limit
    
    if offset + limit >= len(schedules):
        next_offset = offset
    
    if offset - limit <= 0:
        prev_offset = 0

    return schemas.AmortizationSchedule(
        uuid=uuid,
        schedules=schedules[offset:offset+limit],
        next_offset=next_offset,
        prev_offset=prev_offset,
        total=len(schedules)
    )
