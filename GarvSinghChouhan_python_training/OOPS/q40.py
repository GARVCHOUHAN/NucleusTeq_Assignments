"""
Program demonstrating a Student class.
"""


class Student:
    """
    Represents a student with basic details.
    """

    def __init__(
        self,
        name: str,
        age: int,
        branch: str
    ) -> None:
        """
        Initialize student attributes.
        """

        self.name = name
        self.age = age
        self.branch = branch

    def display_details(self) -> None:
        """
        Display student information.
        """

        print("Name:", self.name)
        print("Age:", self.age)
        print("Branch:", self.branch)


if __name__ == "__main__":
    student = Student(
        "Garv",
        21,
        "Information Technology"
    )

    student.display_details()