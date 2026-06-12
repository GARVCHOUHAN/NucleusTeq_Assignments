"""
Program to merge two dictionaries.
"""


def merge_dictionaries() -> None:
    """
    Merge two dictionaries into one.
    """

    first_dictionary: dict[str, int] = {
        "Maths": 90,
        "Science": 85
    }

    second_dictionary: dict[str, int] = {
        "English": 88,
        "Computer": 95
    }

    merged_dictionary: dict[str, int] = (
        first_dictionary | second_dictionary
    )

    print("Merged Dictionary:")
    print(merged_dictionary)


if __name__ == "__main__":
    merge_dictionaries()