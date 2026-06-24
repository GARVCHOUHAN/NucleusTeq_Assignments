"""
NumPy Basics Assignment.

This module demonstrates the basic operations
performed using the NumPy library.
"""

import numpy as np


def create_array() -> np.ndarray:
    """
    Create and return a NumPy array.

    Returns:
        np.ndarray: NumPy array.
    """
    return np.array([10, 20, 30, 40, 50])


def calculate_statistics(numbers: np.ndarray) -> None:
    """
    Display statistical information about the array.

    Args:
        numbers (np.ndarray): Input NumPy array.
    """

    print("Original Array:")
    print(numbers)

    print("\nMean:")
    print(np.mean(numbers))

    print("\nMaximum:")
    print(np.max(numbers))

    print("\nMinimum:")
    print(np.min(numbers))

    print("\nSum:")
    print(np.sum(numbers))


def perform_array_operations() -> None:
    """
    Perform addition and multiplication
    on two NumPy arrays.
    """

    first_array = np.array([1, 2, 3])

    second_array = np.array([4, 5, 6])

    print("\nFirst Array:")
    print(first_array)

    print("\nSecond Array:")
    print(second_array)

    print("\nAddition:")
    print(first_array + second_array)

    print("\nElement-wise Multiplication:")
    print(first_array * second_array)


def create_matrix() -> None:
    """
    Create a 3x3 matrix.
    """

    matrix = np.array([
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ])

    print("\n3 x 3 Matrix:")
    print(matrix)


def main() -> None:
    """
    Execute all NumPy tasks.
    """

    number_array = create_array()

    calculate_statistics(number_array)

    perform_array_operations()

    create_matrix()


if __name__ == "__main__":
    main()