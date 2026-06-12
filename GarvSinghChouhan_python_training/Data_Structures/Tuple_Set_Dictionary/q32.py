"""
Program demonstrating dictionary usage.
"""


def access_student_dictionary() -> None:
    """
    Create a student dictionary
    and access stored values.
    """

    student_information: dict[str, object] = {
        "name": "Garv",
        "age": 21,
        "branch": "Information Technology",
        "cgpa": 7.00
    }

    print("Name:", student_information["name"])
    print("Age:", student_information["age"])
    print("Branch:", student_information["branch"])
    print("CGPA:", student_information["cgpa"])


if __name__ == "__main__":
    access_student_dictionary()