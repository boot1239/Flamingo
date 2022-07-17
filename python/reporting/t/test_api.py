from datetime import datetime

from fastapi.testclient import TestClient

from python.reporting.api import app


client = TestClient(app)


def test_post_event(faker):
    customer_id = faker.uuid4()
    order_id = faker.uuid4()
    response = client.post(
        "/event",
        json={
            "event": {
                "event_name": "order_placed",
                "event_time": str(datetime(2000, 1, 1)),
                "customer_id": customer_id,
                "order_id": order_id,
                "items": [2345, 3456],
                "amount": 34.99,
                "currency": "DKK",
            }
        },
    )
    response.raise_for_status()
    assert response.json() == {
        "stamp": "2022-07-17T09:38:54.934266",
        "event": {
            "event_time": "2000-01-01T00:00:00",
            "customer_id": "e3e70682-c209-4cac-a29f-6fbed82c07cd",
            "order_id": "f728b4fa-4248-4e3a-8a5d-2f346baa9455",
            "items": [2345, 3456],
            "amount": 34.99,
            "currency": "DKK",
            "event_name": "order_placed",
        },
    }
