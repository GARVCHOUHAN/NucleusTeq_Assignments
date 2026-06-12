"""
Program demonstrating tuple creation and access.
"""


def access_tuple_elements() -> None:
    """
    Create a tuple and access its elements.
    """

    student_details: tuple[str, int, str] = (
        "Garv",
        21,
        "Information Technology"
    )

    print("First Element:", student_details[0])
    print("Second Element:", student_details[1])
    print("Third Element:", student_details[2])


if __name__ == "__main__":
    access_tuple_elements()