from typing import List

from pydantic import BaseModel, validator

LENDING_LIMIT_MIN = 1 
LENDING_LIMIT_MAX = 1e9  # one billion
LENDING_RATE_MIN = 0.1
LENDING_RATE_MAX = 99.99
LENDING_TERM_MIN = 1
LENDING_TERM_MAX = 60
NUM_DECIMALS = 2  # rounding outputs


class AmortizationScheduleInput(BaseModel):
    loan_amount: float
    interest_rate: float
    term: int

    @validator('loan_amount')
    def check_amount(cls, amount):
        if amount < LENDING_LIMIT_MIN or amount > LENDING_LIMIT_MAX:
            raise ValueError(f'{amount} is not within the lending amount limits.')
        return amount

    @validator('interest_rate')
    def check_rate(cls, rate):
        if rate < LENDING_RATE_MIN or rate > LENDING_RATE_MAX:
            raise ValueError(f'{rate} is not within than the lending rate limits.')
        return rate

    @validator('term')
    def check_term(cls, term):
        if term < LENDING_LIMIT_MIN or term > LENDING_TERM_MAX:
            raise ValueError(f'{term} is not within the lending term limits.')
        return term


class AmortizationScheduleMonth(BaseModel):
    month: int
    starting_balance: float
    fixed_payment: float
    principal_payment: float
    interest_payment: float
    ending_balance: float
    total_interest: float

    @validator(
        'starting_balance', 
        'fixed_payment', 
        'principal_payment', 
        'interest_payment', 
        'ending_balance', 
        'total_interest'
    )
    def rounded(cls, v):
        return round(v, NUM_DECIMALS)


class AmortizationSchedule(BaseModel):
    uuid: str
    schedules: List[AmortizationScheduleMonth]
    next_offset: int
    prev_offset: int
    total: int