"""
Program demonstrating inheritance.
"""


class Person:
    """
    Parent class representing a person.
    """

    def __init__(
        self,
        name: str,
        age: int
    ) -> None:
        self.name = name
        self.age = age


class Employee(Person):
    """
    Child class inheriting from Person.
    """

    def __init__(
        self,
        name: str,
        age: int,
        employee_id: str
    ) -> None:
        super().__init__(name, age)
        self.employee_id = employee_id

    def display_details(self) -> None:
        """
        Display employee details.
        """

        print("Name:", self.name)
        print("Age:", self.age)
        print("Employee ID:", self.employee_id)


if __name__ == "__main__":
    employee = Employee(
        "Garv",
        21,
        "EMP101"
    )

    employee.display_details()