from abc import ABC
from datetime import datetime
from decimal import Decimal
from typing import List
from typing import Literal
from typing import Optional
from typing import Union
from uuid import UUID

from pydantic import BaseModel
from pydantic import Field

from python.eventbus import models


class BaseEvent(BaseModel, ABC):
    event_time: datetime


class ShoppingCartEvent(BaseEvent, ABC):
    customer_id: Optional[UUID]
    items: List[int]


class ItemAddedToCart(ShoppingCartEvent):
    event_name: Literal["item_added_to_cart"]
    item: int


class ItemRemovedFromCart(ShoppingCartEvent):
    event_name: Literal["item_removed_to_cart"]
    item: int


class OrderEvent(BaseEvent, ABC):
    customer_id: UUID
    order_id: UUID
    items: List[int]
    amount: Decimal
    currency: str


class OrderPlaced(OrderEvent):
    event_name: Literal["order_placed"]


class OrderPaymentStatusUpdated(OrderEvent):
    event_name: Literal["order_payment_status_updated"]
    status: models.OrderPaymentStatus
    message: str


class ParcelEvent(BaseEvent, ABC):
    customer_id: UUID
    order_id: UUID
    parcel_id: UUID
    items: List[int]


class ParcelPickingStatusUpdated(ParcelEvent):
    event_name: Literal["parcel_picking_status_updated"]
    status: models.ParcelPickingStatus
    message: str


class ParcelShippingStatusUpdated(ParcelEvent):
    event_name: Literal["parcel_shipping_status_updated"]
    status: models.ParcelShippingStatus
    message: str


TEvent = Union[
    ItemAddedToCart,
    ItemRemovedFromCart,
    OrderPlaced,
    OrderPaymentStatusUpdated,
    ParcelPickingStatusUpdated,
    ParcelShippingStatusUpdated,
]


class EventEnvelope(BaseModel):
    stamp: datetime = Field(default_factory=datetime.utcnow)
    event: TEvent = Field(..., discriminator="event_name")
