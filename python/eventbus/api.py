from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel

from eventbus.data.envelope import EventEnvelope
from eventbus.data.partition_key import PartitionKey
from eventbus.redis import get_producer

app = FastAPI()


class EventPostResponse(BaseModel):
    event_id: UUID
    status: str = "ok"


@app.post("/event/partition_key/{partition_key}", status_code=201, response_model=EventPostResponse)
def post_event(partition_key: PartitionKey, envelope: EventEnvelope):
    get_producer(partition_key).emit(envelope)
    return EventPostResponse(event_id=envelope.event_id)
