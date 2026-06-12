"""
Program to remove duplicates using set.
"""


def remove_duplicates() -> None:
    """
    Remove duplicate values from a list.
    """

    number_list: list[int] = [10, 20, 10, 30, 20, 40, 50]

    unique_numbers: list[int] = list(set(number_list))

    print("Original List:", number_list)
    print("Unique List:", unique_numbers)


if __name__ == "__main__":
    remove_duplicates()