def fibonacci_recursive(n) -> int:
    """Calculate the nth fibonacci number recursively.

    Args:
        n: nth fibonacci number to calculate

    Returns:
        The nth fibonacci number

    """
    if n in {0, 1}:  # Base case
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
