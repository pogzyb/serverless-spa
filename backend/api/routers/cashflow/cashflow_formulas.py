import logging
from typing import Dict, List, Any

from .cashflow_schemas import AmortizationScheduleInput, AmortizationScheduleMonth


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Amortization:

    def __init__(self, loan_amount: float, term: int, interest_rate: float, round_values: bool = True) -> None:
        self.loan_amount = loan_amount
        self.term = term
        self.interest_rate = interest_rate
        self.round_decimals = round_values

    @classmethod
    def from_schedule_input(cls, schedule_input: AmortizationScheduleInput):
        return cls(**schedule_input.dict())

    def get_monthly_schedule_output(self) -> List[AmortizationScheduleMonth]:
        # schedules contains the 
        schedules: List[AmortizationScheduleMonth] = []
        # convert years to months
        term_in_months = self.years_to_months(self.term)
        # fixed payment does not change month to month
        fixed_payment = self.get_fixed_payment()
        # init total_interest; grows monthly
        total_interest = 0.0        
        for n in range(term_in_months):
            month = n + 1
            starting_balance = self.loan_amount if n == 0 else ending_balance
            if starting_balance < 0:
                fixed_payment = 0
            interest_payment = self.get_interest_payment(starting_balance)
            principal_payment = self.get_principal_payment(fixed_payment, interest_payment)
            ending_balance = self.get_ending_balance(starting_balance, principal_payment)
            total_interest += interest_payment
            # put together data structure output
            month_schedule_values = AmortizationScheduleMonth(
                month=month,
                starting_balance=starting_balance,
                ending_balance=ending_balance,
                interest_payment=interest_payment,
                principal_payment=principal_payment,
                fixed_payment=fixed_payment,
                total_interest=total_interest
            )
            schedules.append(month_schedule_values)
        return schedules

    @staticmethod
    def years_to_months(yrs: int):
        return yrs * 12

    @staticmethod
    def rate_as_decimal(r: float):
        return r / 100

    def get_fixed_payment(self) -> float:
        months = self.years_to_months(self.term)
        rate = self.rate_as_decimal(self.interest_rate) / 12
        return self.loan_amount * ( rate * (1 + rate)**months ) / ( (1 + rate)**months - 1 )
        
    def get_starting_balance(self, month: int, principal_payment: float) -> float:
        v = self.loan_amount - ( ( month - 1 ) * principal_payment )
        return round(v, 2)

    def get_ending_balance(self, starting_balance: float, principal_payment: float) -> float:
        v = starting_balance - principal_payment
        return round(v, 2)

    def get_interest_payment(self, starting_balance: float) -> float:
        rate = self.rate_as_decimal(self.interest_rate)
        v = starting_balance * (rate / 12)
        return round(v, 2)

    def get_principal_payment(self, fixed_payment: float, interest_payment: float) -> float:
        v = fixed_payment - interest_payment
        return round(v, 2)
    