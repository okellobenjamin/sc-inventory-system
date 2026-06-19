import pytest

from inventory import calculate_restock_order


# --- Happy path / correctness tests ---

def test_standard_order_not_high_velocity() -> None:
    # 45 in stock, refill to 100 -> needs 55 -> rounds up to nearest 10 = 60
    assert calculate_restock_order(45, 50, 100, False, 10) == 60


def test_standard_order_high_velocity() -> None:
    # base 55, +15% (9 units) = 64 -> rounds up to nearest 10 = 70
    assert calculate_restock_order(45, 50, 100, True, 10) == 70


def test_no_order_when_stock_above_reorder_point() -> None:
    # stock (60) is above the reorder point (50), so nothing is ordered
    assert calculate_restock_order(60, 50, 100, False, 10) == 0


# --- Defensive / edge-case tests ---

def test_negative_stock_raises_value_error() -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        calculate_restock_order(-1, 50, 100, False, 10)


def test_zero_batch_size_raises_value_error() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        calculate_restock_order(20, 50, 100, False, 0)


def test_max_not_above_reorder_raises_value_error() -> None:
    with pytest.raises(ValueError, match="greater than reorder_point"):
        calculate_restock_order(20, 50, 50, False, 10)


def test_non_integer_stock_raises_type_error() -> None:
    with pytest.raises(TypeError, match="must be an integer"):
        calculate_restock_order("20", 50, 100, False, 10)