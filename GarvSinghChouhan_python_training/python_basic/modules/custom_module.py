"""
Custom utility module for number-related operations.
"""


def is_prime(number: int) -> bool:
    """
    Check whether a number is prime.

    Args:
        number: Number to be checked.

    Returns:
        True if the number is prime, otherwise False.
    """

    if number <= 1:
        return False

    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False

    return True