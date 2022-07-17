from functools import lru_cache
from typing import Iterable
from typing import List

from redis import Redis

from eventbus.data.envelope import EventEnvelope
from eventbus.data.partition_key import PartitionKey


redis = Redis()


class RedisConsumer:
    def __init__(self, partition_keys: List[PartitionKey]):
        self.subscriber = redis.pubsub()
        self.subscriber.subscribe(*partition_keys)

    def get_events(self) -> Iterable[EventEnvelope]:
        while message := self.subscriber.get_message():
            if message['type'] != 'message':
                continue

            yield EventEnvelope.parse_raw(message['data'])


class RedisProducer:
    def __init__(self, partition_key: PartitionKey):
        self.partition_key = partition_key

    def emit(self, envelope: EventEnvelope):
        redis.publish(self.partition_key, envelope.json())


@lru_cache
def get_producer(partition_key: PartitionKey) -> RedisProducer:
    return RedisProducer(partition_key)
