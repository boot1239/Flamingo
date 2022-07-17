# Flamingo

The main isssue with Flamingo is automatic data sharing is missing. This is seen in these places:
- The customers don't have a single interface where all relevant information is displayed
- Notifications aren't streamlined and shown to customers in a single place
- The data team doesn't have a single place to gather relevant data from


## Eventbus solution

I present an eventbus solution to fix all three issues by maing sure data is shared between all relevant entities in the system.

![Eventbus drawio](https://user-images.githubusercontent.com/47638416/179398117-208a6f9a-9099-46d5-9c0e-643a4686c6ce.png)

For all actions in the three systems Webshop, Payments and Fulfillment and event is sent to the eventbus, they are producers of events. The eventbus is then setup so that all who need any information from these systems can then subsribe to specific events from the producers and become consumers in the system.

An example of an event could be an ItemAddedToCartEvent which indicates that an item in the webshop has been added to a shopping cart containing a list of items already. All events have an `event_time` attribute which indicates when the event happened.

```
class BaseEvent(BaseModel, ABC):
    event_time: datetime


class ShoppingCartEvent(BaseEvent, ABC):
    customer_id: Optional[UUID]
    items: List[int]


class ItemAddedToCart(ShoppingCartEvent):
    event_name: Literal["item_added_to_cart"]
    item: int
```

Events are all contained within an EventEnvelope which contain some event meta data along with a stamp of event creation.

```
class EventEnvelope(BaseModel):
    event_id: UUID
    stamp: datetime = Field(default_factory=datetime.utcnow)
    event: TEvent = Field(..., discriminator="event_name")
```


## Customer order information and notifications

All events with order information relevant to customers are then fed back into a subsystem of the webshop, so that customers can log into a single place and see all information about their orders. This place will then also be responsible for notifying customers of important updates relating to their orders.


## Data team reporting

A new system will be created for the use of the datateam where a single database with all information relevant to the team will be stored. This will mean that they only have to query a single system for data and the data can be stored in the most appropiate fashion for the team.

```
class EventPostResponse(BaseModel):
    event_id: UUID
    status: str = "ok"


@app.post("/event", status_code=201, response_model=EventPostResponse)
def post_event(envelope: EventEnvelope):
    save_event_to_db(envelope)
    return EventPostResponse(event_id=envelope.event_id)
```


## Drawbacks

A downside of having an event bus is the time and energy required to make sure all parties agree on the events and that all new events will be implemented for all interested parties.

It also requires some careful planning and structuring of both the eventbus and all consumers to make sure no system is overloaded with events and that the delay of events will never exceed an important threshold.

