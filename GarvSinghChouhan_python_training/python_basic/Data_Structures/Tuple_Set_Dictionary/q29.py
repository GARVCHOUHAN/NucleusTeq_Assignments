"""
Program to convert tuple into list and modify it.
"""


def modify_tuple_data() -> None:
    """
    Convert tuple into list and update data.
    """

    programming_languages: tuple[str, ...] = (
        "Python",
        "Java",
        "C++"
    )

    language_list: list[str] = list(programming_languages)

    language_list.append("JavaScript")

    print("Original Tuple:", programming_languages)
    print("Modified List:", language_list)


if __name__ == "__main__":
    modify_tuple_data()