
"""
Student Performance Analysis Mini Project

This module demonstrates an end-to-end data analysis
using Pandas, Matplotlib, and Seaborn.
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PASS_MARKS = 65


def create_student_dataframe() -> pd.DataFrame:
    """
    Create and return a student DataFrame.

    Returns:
        pd.DataFrame: Student DataFrame.
    """

    student_data = {
        "Name": [
            "Rahul",
            "Priya",
            "Siri",
            "Anuj"
        ],
        "Marks": [
            70,
            80,
            90,
            60
        ],
        "Hours Studied": [
            2,
            3,
            5,
            1
        ]
    }

    return pd.DataFrame(student_data)


def add_performance_column(student_dataframe: pd.DataFrame) -> None:
    """
    Add Performance column based on marks.

    Args:
        student_dataframe (pd.DataFrame):
            Student DataFrame.
    """

    # Assign Pass or Fail based on marks
    student_dataframe["Performance"] = student_dataframe[
        "Marks"
    ].apply(
        lambda marks: "Pass"
        if marks > PASS_MARKS
        else "Fail"
    )

    print("\nStudent DataFrame:")
    print(student_dataframe)


def create_line_chart(student_dataframe: pd.DataFrame) -> None:
    """
    Create a line chart for
    Hours Studied vs Marks.

    Args:
        student_dataframe (pd.DataFrame):
            Student DataFrame.
    """

    plt.figure(figsize=(7, 5))

    plt.plot(
        student_dataframe["Hours Studied"],
        student_dataframe["Marks"],
        marker="o",
        linewidth=2
    )

    plt.title("Hours Studied vs Marks")
    plt.xlabel("Hours Studied")
    plt.ylabel("Marks")

    plt.grid(True)

    plt.show()


def create_scatter_plot(student_dataframe: pd.DataFrame) -> None:
    """
    Create a scatter plot for
    Hours Studied vs Marks.

    Args:
        student_dataframe (pd.DataFrame):
            Student DataFrame.
    """

    plt.figure(figsize=(7, 5))

    plt.scatter(
        student_dataframe["Hours Studied"],
        student_dataframe["Marks"],
        color="red",
        s=120
    )

    plt.title("Study Hours vs Marks")
    plt.xlabel("Hours Studied")
    plt.ylabel("Marks")

    plt.grid(True)

    plt.show()


def create_bar_plot(student_dataframe: pd.DataFrame) -> None:
    """
    Create a Seaborn bar plot
    showing Performance vs Marks.

    Args:
        student_dataframe (pd.DataFrame):
            Student DataFrame.
    """

    plt.figure(figsize=(7, 5))

    sns.barplot(
        data=student_dataframe,
        x="Performance",
        y="Marks"
    )

    plt.title("Performance vs Marks")

    plt.show()


def main() -> None:
    """
    Execute the complete
    student performance analysis.
    """

    # Create student dataset
    student_dataframe = create_student_dataframe()

    # Add performance status
    add_performance_column(
        student_dataframe
    )

    # Generate visualizations
    create_line_chart(
        student_dataframe
    )

    create_scatter_plot(
        student_dataframe
    )

    create_bar_plot(
        student_dataframe
    )


if __name__ == "__main__":
    main()

