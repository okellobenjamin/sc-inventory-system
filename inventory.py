import math


def calculate_restock_order(
    current_stock: int,
    reorder_point: int,
    max_capacity: int,
    high_velocity: bool,
    supplier_batch_size: int,
) -> int:
    """Work out how many units to reorder from the supplier.

    The order refills stock up to max_capacity, adds a 15% safety
    premium for high-velocity items, then rounds up to the supplier's
    fixed batch size. Returns 0 when no reorder is needed.
    """
    # Type checks: numeric inputs must be whole numbers, not text, floats
    # or booleans (in Python True/False count as ints, so we rule them out).
    if not isinstance(current_stock, int) or isinstance(current_stock, bool):
        raise TypeError("current_stock must be an integer")
    if not isinstance(reorder_point, int) or isinstance(reorder_point, bool):
        raise TypeError("reorder_point must be an integer")
    if not isinstance(max_capacity, int) or isinstance(max_capacity, bool):
        raise TypeError("max_capacity must be an integer")
    if not isinstance(supplier_batch_size, int) or isinstance(supplier_batch_size, bool):
        raise TypeError("supplier_batch_size must be an integer")
    if not isinstance(high_velocity, bool):
        raise TypeError("high_velocity must be a boolean")

    # Value checks: guard against impossible inputs.
    if current_stock < 0:
        raise ValueError("current_stock cannot be negative")
    if reorder_point < 0:
        raise ValueError("reorder_point cannot be negative")
    if max_capacity < 0:
        raise ValueError("max_capacity cannot be negative")
    if supplier_batch_size <= 0:
        raise ValueError("supplier_batch_size must be greater than zero")
    if max_capacity <= reorder_point:
        raise ValueError("max_capacity must be greater than reorder_point")

    # No reorder needed while stock is still at or above the reorder point.
    if current_stock >= reorder_point:
        return 0

    # Base order: enough units to refill back up to max_capacity.
    order_quantity = max_capacity - current_stock

    # Velocity premium: add 15% safety stock, rounded up to a whole unit.
    if high_velocity:
        order_quantity += math.ceil(order_quantity * 15 / 100)

    # Supplier batch: round the order up to the nearest batch multiple.
    batches_needed = math.ceil(order_quantity / supplier_batch_size)
    return batches_needed * supplier_batch_size