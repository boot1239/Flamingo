from __future__ import annotations

from fastapi import FastAPI

from python.eventbus import events

app = FastAPI()


@app.post("/event")
def post_event(envelope: events.EventEnvelope):
    return envelope
