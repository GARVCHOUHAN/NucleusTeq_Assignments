"""
Pandas DataFrame Assignment.

This module demonstrates basic DataFrame creation
and operations using the Pandas library.
"""

import pandas as pd


BONUS_PERCENTAGE = 0.10


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


def display_first_two_rows(
    employee_dataframe: pd.DataFrame
) -> None:
    """
    Display the first two rows.

    Args:
        employee_dataframe (pd.DataFrame):
            Employee DataFrame.
    """

    print("\nFirst Two Rows:")
    print(employee_dataframe.head(2))


def display_summary_statistics(
    employee_dataframe: pd.DataFrame
) -> None:
    """
    Display summary statistics.

    Args:
        employee_dataframe (pd.DataFrame):
            Employee DataFrame.
    """

    print("\nSummary Statistics:")
    print(employee_dataframe.describe())


def display_it_employees(
    employee_dataframe: pd.DataFrame
) -> None:
    """
    Display employees from IT department.

    Args:
        employee_dataframe (pd.DataFrame):
            Employee DataFrame.
    """

    it_employees = employee_dataframe[
        employee_dataframe["Department"] == "IT"
    ]

    print("\nIT Employees:")
    print(it_employees)


def add_bonus_column(
    employee_dataframe: pd.DataFrame
) -> None:
    """
    Add Bonus column.

    Args:
        employee_dataframe (pd.DataFrame):
            Employee DataFrame.
    """

    employee_dataframe["Bonus"] = (
        employee_dataframe["Salary"]
        * BONUS_PERCENTAGE
    )

    print("\nEmployee DataFrame with Bonus:")
    print(employee_dataframe)


def main() -> None:
    """
    Execute all DataFrame operations.
    """

    employee_dataframe = create_employee_dataframe()

    print("Employee DataFrame:")
    print(employee_dataframe)

    display_first_two_rows(
        employee_dataframe
    )

    display_summary_statistics(
        employee_dataframe
    )

    display_it_employees(
        employee_dataframe
    )

    add_bonus_column(
        employee_dataframe
    )


if __name__ == "__main__":
    main()