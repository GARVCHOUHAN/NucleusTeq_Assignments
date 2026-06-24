git 
"""
Seaborn Visualization Assignment

This module demonstrates different visualization
techniques using the Seaborn library.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


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


def create_bar_plot(employee_dataframe: pd.DataFrame) -> None:
    """
    Create a bar plot showing
    Department vs Salary.

    Args:
        employee_dataframe (pd.DataFrame):
            Employee DataFrame.
    """

    # Create bar plot
    plt.figure(figsize=(7, 5))

    sns.barplot(
        data=employee_dataframe,
        x="Department",
        y="Salary"
    )

    plt.title("Department vs Salary")

    plt.show()


def create_box_plot(employee_dataframe: pd.DataFrame) -> None:
    """
    Create a box plot showing
    salary distribution.

    Args:
        employee_dataframe (pd.DataFrame):
            Employee DataFrame.
    """

    # Create box plot
    plt.figure(figsize=(7, 5))

    sns.boxplot(
        data=employee_dataframe,
        y="Salary"
    )

    plt.title("Salary Distribution")

    plt.show()


def create_heatmap(employee_dataframe: pd.DataFrame) -> None:
    """
    Create a heatmap showing
    correlation between Age and Salary.

    Args:
        employee_dataframe (pd.DataFrame):
            Employee DataFrame.
    """

    # Calculate correlation matrix
    correlation_matrix = employee_dataframe[
        [
            "Age",
            "Salary"
        ]
    ].corr()

    # Create heatmap
    plt.figure(figsize=(6, 5))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="Blues"
    )

    plt.title("Correlation Heatmap")

    plt.show()


def main() -> None:
    """
    Execute all Seaborn visualizations.
    """

    employee_dataframe = create_employee_dataframe()

    create_bar_plot(
        employee_dataframe
    )

    create_box_plot(
        employee_dataframe
    )

    create_heatmap(
        employee_dataframe
    )


if __name__ == "__main__":
    main()

