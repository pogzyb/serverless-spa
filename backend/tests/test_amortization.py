from unittest import TestCase

from api.routers.cashflow.cashflow_formulas import Amortization


class TestAmortization(TestCase):

    def setUp(self) -> None:
        amount = 250000
        term = 10
        rate = 5.0
        # make client
        self.client = Amortization(amount, term, rate)
        return super().setUp()

    def test_get_starting_balance(self):
        # check starting balances
        month = 1
        principal_pmt = 1000
        starting_balance = self.client.get_starting_balance(month, principal_pmt)
        self.assertEqual(starting_balance, self.client.loan_amount, f"{starting_balance} != {self.client.loan_amount}")
        # check starting balance at 5 month mark
        month = 5
        expected_amount = self.client.loan_amount - ( (month - 1) * principal_pmt)
        starting_balance = self.client.get_starting_balance(month, principal_pmt)
        self.assertEqual(starting_balance, expected_amount, f"{starting_balance} != {expected_amount}")

    def test_get_ending_balance(self):
        month = 1
        principal_pmt = 1000
        expected_ending_balance = self.client.loan_amount - (month * principal_pmt)
        ending_balance = self.client.get_ending_balance(month, principal_pmt)
        self.assertEqual(ending_balance, expected_ending_balance, f"{ending_balance} != {expected_ending_balance}")
        # check month 5
        month = 5
        principal_pmt = 1000
        expected_ending_balance = self.client.loan_amount - (month * principal_pmt)
        ending_balance = self.client.get_ending_balance(month, principal_pmt)
        self.assertEqual(ending_balance, expected_ending_balance, f"{ending_balance} != {expected_ending_balance}")

    def test_get_principal_payment(self):
        fixed_pmt = 1000
        interest_pmt = 500
        expected_principal = fixed_pmt - interest_pmt
        principal_payment = self.client.get_principal_payment(fixed_pmt, interest_pmt)
        self.assertEqual(principal_payment, expected_principal, f'{principal_payment} != {expected_principal}')

    def test_get_interest_payment(self):
        # with client defaults
        expected_interest_pmt = self.client.loan_amount * 0.05 / 12
        interest_pmt = self.client.get_interest_payment(self.client.loan_amount)
        self.assertEqual(interest_pmt, expected_interest_pmt, f'{interest_pmt} != {expected_interest_pmt}')
        # with starting balance of 10k
        interest_pmt = self.client.get_interest_payment(10000)
        expected_interest_pmt = 10000 * 0.05 / 12
        self.assertEqual(interest_pmt, expected_interest_pmt, f'{interest_pmt} != {expected_interest_pmt}')

    def test_fixed_payment(self):
        expected_fixed_pmt = 2651.64
        default_fixed_pmt = round(self.client.get_fixed_payment(), 2)
        self.assertEqual(default_fixed_pmt, expected_fixed_pmt, f'{default_fixed_pmt} != {expected_fixed_pmt}')
        # update client defaults
        self.client.term = 30
        self.client.interest_rate = 3.625
        expected_fixed_pmt = 1140.13
        fixed_pmt = round(self.client.get_fixed_payment(), 2)
        self.assertEqual(fixed_pmt, expected_fixed_pmt, f'{fixed_pmt} != {expected_fixed_pmt}')


