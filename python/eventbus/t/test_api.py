from datetime import datetime

from fastapi.testclient import TestClient

from python.eventbus.api import app


client = TestClient(app)


def test_post_event(faker):
    event_id = faker.uuid4()
    response = client.post(
        "/event/partition_key/webshop_order",
        json={
            "event_id": event_id,
            "event": {
                "event_name": "order_placed",
                "event_time": str(datetime(2000, 1, 1)),
                "customer_id": faker.uuid4(),
                "order_id": faker.uuid4(),
                "items": [2345, 3456],
                "amount": 34.99,
                "currency": "DKK",
            }
        },
    )
    response.raise_for_status()
    assert response.json() == {"status": "ok", "event_id": event_id}
