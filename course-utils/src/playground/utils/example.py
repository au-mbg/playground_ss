def proportional_response(value: float, *, rate: float) -> float:
    """Return the response predicted by ``response = rate * value``."""
    return rate * value
