from datetime import datetime

from eventbus.data.envelope import EventEnvelope
from eventbus.data.partition_key import PartitionKey
from eventbus.redis import RedisConsumer
from eventbus.redis import RedisProducer


def test_redis_pub_sub(faker):
    webshop = RedisProducer(PartitionKey.webshop_cart)
    reporting = RedisConsumer([PartitionKey.webshop_cart])
    event = EventEnvelope.parse_obj(
        {
            "event_id": faker.uuid4(),
            "event": {
                "event_name": "order_placed",
                "event_time": str(datetime(2000, 1, 1)),
                "customer_id": faker.uuid4(),
                "order_id": faker.uuid4(),
                "items": [2345, 3456],
                "amount": 34.99,
                "currency": "DKK",
            },
        },
    )
    webshop.emit(event)

    assert list(reporting.get_events()) == [event]
