from enum import Enum


class PartitionKey(str, Enum):
    webshop_cart = "webshop-cart"
    webshop_order = "webshop-order"
