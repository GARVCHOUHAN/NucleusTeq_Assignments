### Question 37: Append Data to Existing File

"""
Program to append data to an existing file.
"""


def append_data_to_file() -> None:
    """
    Append new content to a file.
    """

    with open("student.txt", "a", encoding="utf-8") as file:
        file.write("\nPython Training Assignment")

    print("Data appended successfully.")


if __name__ == "__main__":
    append_data_to_file()