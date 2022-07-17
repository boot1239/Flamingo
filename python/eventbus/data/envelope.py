from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field

from eventbus.data.events import TEvent


class EventEnvelope(BaseModel):
    event_id: UUID
    stamp: datetime = Field(default_factory=datetime.utcnow)
    event: TEvent = Field(..., discriminator="event_name")
