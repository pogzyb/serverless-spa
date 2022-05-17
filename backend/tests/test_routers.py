from fastapi.testclient import TestClient

from api import create_app
from api.routers.cashflow.cashflow_schemas import AmortizationSchedule


client = TestClient(create_app())
fake_payload = {
    'loan_amount': 250000,
    'term': 30,
    'interest_rate': 3.625
}

def test_calc_schedule():
    response = client.post("/cashflow/calc-schedule", json=fake_payload)
    # check ok
    assert response.status_code == 200
    # check all expected keys exist; parse_obj will raise exception otherwise
    AmortizationSchedule.parse_obj(response.json())


def test_get_schedule():
    response = client.post("/cashflow/calc-schedule", json=fake_payload)
    # check ok
    assert response.status_code == 200
    # check offset values
    schedule = AmortizationSchedule.parse_obj(response.json())
    assert schedule.next_offset == 12



