import sys
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from commissioning_mbo import Book


@settings(max_examples=50, derandomize=True)
@given(st.lists(st.integers(min_value=1, max_value=10000), min_size=1, max_size=30))
def test_add_and_cancel_preserves_all_volume(quantities):
    b = Book()
    for i, q in enumerate(quantities):
        b.apply(
            {
                "sequence": i + 1,
                "type": "add",
                "id": str(i),
                "side": "bid",
                "price": 100,
                "quantity": q,
            }
        )
    assert b.levels() == {"bid": {100: sum(quantities)}, "ask": {}}
    for i in reversed(range(len(quantities))):
        b.apply({"sequence": b.sequence + 1, "type": "cancel", "id": str(i)})
    assert b.levels() == {"bid": {}, "ask": {}}
    assert not b.orders


@settings(max_examples=50, derandomize=True)
@given(
    st.integers(min_value=1, max_value=10000), st.integers(min_value=1, max_value=10000)
)
def test_overfill_is_atomic(quantity, excess):
    b = Book()
    b.apply(
        {
            "sequence": 1,
            "type": "add",
            "id": "one",
            "side": "ask",
            "price": 100,
            "quantity": quantity,
        }
    )
    before = b.snapshot()
    with pytest.raises(ValueError):
        b.apply(
            {"sequence": 2, "type": "fill", "id": "one", "quantity": quantity + excess}
        )
    assert b.snapshot() == before
    b.apply({"sequence": 2, "type": "fill", "id": "one", "quantity": quantity})
    assert not b.orders
    assert b.traded_volume == quantity
