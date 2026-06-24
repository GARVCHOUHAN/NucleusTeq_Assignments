
"""
Data Analysis Assignment

This module demonstrates GroupBy operations
using the Pandas library.
"""

import pandas as pd


def create_employee_dataframe() -> pd.DataFrame:
    """
    Create and return an employee DataFrame.

    Returns:
        pd.DataFrame: Employee DataFrame.
    """

    employee_data = {
        "Name": [
            "Rahul",
            "Priya",
            "Amit",
            "Anuj"
        ],
        "Age": [
            25,
            30,
            28,
            35
        ],
        "Department": [
            "HR",
            "IT",
            "Finance",
            "IT"
        ],
        "Salary": [
            30000,
            50000,
            45000,
            60000
        ]
    }

    return pd.DataFrame(employee_data)


def find_average_salary(employee_dataframe: pd.DataFrame) -> None:
    """
    Display average salary for each department.

    Args:
        employee_dataframe (pd.DataFrame):
            Employee DataFrame.
    """

    # Calculate average salary department-wise
    average_salary = employee_dataframe.groupby(
        "Department"
    )["Salary"].mean()

    print("\nAverage Salary By Department:")
    print(average_salary)


def find_maximum_salary(employee_dataframe: pd.DataFrame) -> None:
    """
    Display maximum salary for each department.

    Args:
        employee_dataframe (pd.DataFrame):
            Employee DataFrame.
    """

    # Calculate maximum salary department-wise
    maximum_salary = employee_dataframe.groupby(
        "Department"
    )["Salary"].max()

    print("\nMaximum Salary By Department:")
    print(maximum_salary)


def count_employees(employee_dataframe: pd.DataFrame) -> None:
    """
    Count employees in each department.

    Args:
        employee_dataframe (pd.DataFrame):
            Employee DataFrame.
    """

    # Count total employees in every department
    employee_count = employee_dataframe.groupby(
        "Department"
    )["Name"].count()

    print("\nEmployee Count By Department:")
    print(employee_count)


def main() -> None:
    """
    Execute all GroupBy operations.
    """

    # Create employee DataFrame
    employee_dataframe = create_employee_dataframe()

    print("Employee DataFrame:")
    print(employee_dataframe)

    # Display average salary
    find_average_salary(employee_dataframe)

    # Display maximum salary
    find_maximum_salary(employee_dataframe)

    # Display employee count
    count_employees(employee_dataframe)


if __name__ == "__main__":
    main()
