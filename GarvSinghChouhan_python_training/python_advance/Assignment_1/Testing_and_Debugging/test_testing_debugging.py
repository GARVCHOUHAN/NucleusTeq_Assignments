"""
Pytest test cases.
"""

from testing_debugging import (
    add_numbers,
    is_prime
)


def test_add_numbers_positive() -> None:

    assert add_numbers(10, 20) == 30


def test_add_numbers_negative() -> None:

    assert add_numbers(-5, -5) == -10


def test_add_numbers_zero() -> None:

    assert add_numbers(10, 0) == 10


def test_prime_number() -> None:

    assert is_prime(11) is True


def test_non_prime_number() -> None:

    assert is_prime(12) is False


def test_prime_edge_case() -> None:

    assert is_prime(2) is True


def test_non_prime_edge_case() -> None:

    assert is_prime(1) is False