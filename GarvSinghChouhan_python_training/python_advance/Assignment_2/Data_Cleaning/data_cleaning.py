
"""
Data Cleaning Assignment

This module demonstrates how to detect and handle
missing values using the Pandas library.
"""

import pandas as pd


DEFAULT_SALARY = 0


def create_employee_dataframe() -> pd.DataFrame:
    """
    Create an employee DataFrame containing
    missing values.

    Returns:
        pd.DataFrame: Employee DataFrame.
    """

    employee_data = {
        "Name": [
            "Rahul",
            "Priya",
            "Anuj"
        ],
        "Age": [
            25,
            None,
            29
        ],
        "Salary": [
            30000,
            40000,
            None
        ]
    }

    return pd.DataFrame(employee_data)


def detect_missing_values(employee_dataframe: pd.DataFrame) -> None:
    """
    Display all missing values present
    in the DataFrame.

    Args:
        employee_dataframe (pd.DataFrame):
            Employee DataFrame.
    """

    print("\nOriginal DataFrame:")
    print(employee_dataframe)

    # Check every column for missing values
    print("\nMissing Values:")
    print(employee_dataframe.isnull())


def replace_missing_age(employee_dataframe: pd.DataFrame) -> None:
    """
    Replace missing Age values
    with the average age.

    Args:
        employee_dataframe (pd.DataFrame):
            Employee DataFrame.
    """

    # Calculate average age by ignoring missing values
    average_age = employee_dataframe["Age"].mean()

    # Fill missing Age values with calculated average
    employee_dataframe["Age"] = employee_dataframe[
        "Age"
    ].fillna(average_age)

    print("\nAfter Replacing Missing Age:")
    print(employee_dataframe)


def replace_missing_salary(employee_dataframe: pd.DataFrame) -> None:
    """
    Replace missing Salary values with
    the default salary.

    Args:
        employee_dataframe (pd.DataFrame):
            Employee DataFrame.
    """

    # Replace missing Salary values with 0
    employee_dataframe["Salary"] = employee_dataframe[
        "Salary"
    ].fillna(DEFAULT_SALARY)

    print("\nAfter Replacing Missing Salary:")
    print(employee_dataframe)


def main() -> None:
    """
    Execute all data cleaning operations.
    """

    # Create sample employee data
    employee_dataframe = create_employee_dataframe()

    # Display missing values
    detect_missing_values(employee_dataframe)

    # Replace missing Age with average Age
    replace_missing_age(employee_dataframe)

    # Replace missing Salary with default value
    replace_missing_salary(employee_dataframe)


if __name__ == "__main__":
    main()

