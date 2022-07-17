from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel

from eventbus.data.envelope import EventEnvelope

app = FastAPI()


def save_event_to_db(envelope: EventEnvelope):
    """Saves data in event to data reporting DB"""
    pass


class EventPostResponse(BaseModel):
    event_id: UUID
    status: str = "ok"


@app.post("/event", status_code=201, response_model=EventPostResponse)
def post_event(envelope: EventEnvelope):
    save_event_to_db(envelope)
    return EventPostResponse(event_id=envelope.event_id)
