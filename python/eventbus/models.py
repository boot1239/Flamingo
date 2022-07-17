from enum import Enum


class OrderPaymentStatus(str, Enum):
    accepted = "accepted"
    declined = "declined"
    error = "error"


class ParcelPickingStatus(str, Enum):
    picked = "picked"
    packed = "packed"
    incomplete = "incomplete"
    missing = "missing"


class ParcelShippingStatus(str, Enum):
    ready_for_pickup = "ready-for-pickup"
    picked_up = "picked-up"
    transferred = "transferred"
    delivered = "delivered"
    lost = "lost"
