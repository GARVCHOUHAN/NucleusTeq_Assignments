"""
Program to perform set operations.
"""


def perform_set_operations() -> None:
    """
    Perform union, intersection,
    and difference operations.
    """

    first_set: set[int] = {1, 2, 3, 4, 5}
    second_set: set[int] = {4, 5, 6, 7, 8}

    print("Union:", first_set.union(second_set))
    print("Intersection:", first_set.intersection(second_set))
    print("Difference:", first_set.difference(second_set))


if __name__ == "__main__":
    perform_set_operations()