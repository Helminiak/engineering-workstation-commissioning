"""Synthetic order-event reference model. Integer ticks; not a CME decoder."""

import copy
from dataclasses import dataclass, replace


@dataclass
class Order:
    side: str
    price: int
    quantity: int
    priority: int


class Book:
    def __init__(self):
        self.orders = {}
        self.sequence = 0
        self.traded_volume = 0
        self.delta = 0

    def apply(self, event):
        e = dict(event)
        seq = e["sequence"]
        if seq != self.sequence + 1:
            raise ValueError("Missing or out-of-order sequence")
        old = copy.deepcopy(self.orders)
        volume = self.traded_volume
        delta = self.delta
        try:
            kind = e["type"]
            oid = e.get("id")
            q = e.get("quantity")
            if kind == "add":
                if (
                    oid in self.orders
                    or e["side"] not in ("bid", "ask")
                    or q <= 0
                    or e["price"] <= 0
                ):
                    raise ValueError("Invalid new order")
                self.orders[oid] = Order(e["side"], e["price"], q, seq)
            elif kind == "modify":
                o = self.orders[oid]
                if q <= 0 or e["price"] <= 0:
                    raise ValueError("Invalid modify")
                priority = (
                    seq if q > o.quantity or e["price"] != o.price else o.priority
                )
                self.orders[oid] = replace(
                    o, price=e["price"], quantity=q, priority=priority
                )
            elif kind == "cancel":
                del self.orders[oid]
            elif kind == "fill":
                o = self.orders[oid]
                if q <= 0 or q > o.quantity:
                    raise ValueError("Invalid fill")
                self.traded_volume += q
                self.delta += q if o.side == "ask" else -q
                if q == o.quantity:
                    del self.orders[oid]
                else:
                    self.orders[oid] = replace(o, quantity=o.quantity - q)
            elif kind == "trade":
                if q <= 0 or e.get("aggressor") not in ("buy", "sell"):
                    raise ValueError("Invalid trade")
                self.traded_volume += q
                self.delta += q if e["aggressor"] == "buy" else -q
            else:
                raise ValueError("Unknown event type")
            bids = [o.price for o in self.orders.values() if o.side == "bid"]
            asks = [o.price for o in self.orders.values() if o.side == "ask"]
            if bids and asks and max(bids) >= min(asks):
                raise ValueError("Locked/crossed book")
        except Exception:
            self.orders = old
            self.traded_volume = volume
            self.delta = delta
            raise
        self.sequence = seq

    def levels(self):
        result = {"bid": {}, "ask": {}}
        for o in self.orders.values():
            result[o.side][o.price] = result[o.side].get(o.price, 0) + o.quantity
        return result

    def queue(self, side, price):
        return [
            oid
            for oid, o in sorted(self.orders.items(), key=lambda item: item[1].priority)
            if o.side == side and o.price == price
        ]

    def snapshot(self):
        return {
            "sequence": self.sequence,
            "orders": {k: vars(v) for k, v in sorted(self.orders.items())},
            "levels": self.levels(),
            "traded_volume": self.traded_volume,
            "delta": self.delta,
        }
