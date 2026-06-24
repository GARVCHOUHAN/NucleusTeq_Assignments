
"""
Matplotlib Charts Assignment

This module demonstrates how to create
different charts using the Matplotlib library.
"""

import matplotlib.pyplot as plt


def create_bar_chart() -> None:
    """
    Create a bar chart showing the
    number of employees in each department.
    """

    departments = [
        "HR",
        "IT",
        "Finance"
    ]

    employees = [
        5,
        12,
        7
    ]

    # Create bar chart
    plt.figure(figsize=(6, 5))

    plt.bar(
        departments,
        employees,
        color=[
            "skyblue",
            "orange",
            "green"
        ]
    )

    plt.title("Employees by Department")
    plt.xlabel("Department")
    plt.ylabel("Number of Employees")

    plt.show()


def create_line_chart() -> None:
    """
    Create a line chart showing
    employee count by department.
    """

    departments = [
        "HR",
        "IT",
        "Finance"
    ]

    employees = [
        5,
        12,
        7
    ]

    # Create line chart
    plt.figure(figsize=(6, 5))

    plt.plot(
        departments,
        employees,
        marker="o",
        linewidth=2
    )

    plt.title("Employees by Department")
    plt.xlabel("Department")
    plt.ylabel("Number of Employees")

    plt.grid(True)

    plt.show()


def create_histogram() -> None:
    """
    Create a histogram using
    employee salary data.
    """

    salaries = [
        30000,
        40000,
        50000,
        60000,
        45000
    ]

    # Create histogram
    plt.figure(figsize=(6, 5))

    plt.hist(
        salaries,
        bins=5,
        edgecolor="black"
    )

    plt.title("Salary Distribution")
    plt.xlabel("Salary")
    plt.ylabel("Frequency")

    plt.show()


def create_scatter_plot() -> None:
    """
    Create a scatter plot showing
    Age vs Salary.
    """

    ages = [
        25,
        30,
        28,
        35
    ]

    salaries = [
        30000,
        50000,
        45000,
        60000
    ]

    # Create scatter plot
    plt.figure(figsize=(6, 5))

    plt.scatter(
        ages,
        salaries,
        s=100,
        color="red"
    )

    plt.title("Age vs Salary")
    plt.xlabel("Age")
    plt.ylabel("Salary")

    plt.grid(True)

    plt.show()


def main() -> None:
    """
    Execute all chart creation functions.
    """

    create_bar_chart()

    create_line_chart()

    create_histogram()

    create_scatter_plot()


if __name__ == "__main__":
    main()

