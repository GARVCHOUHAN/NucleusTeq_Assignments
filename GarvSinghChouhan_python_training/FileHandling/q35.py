### Create a File and Write Your Name into It


"""
Program to create a file and write data into it.
"""


def write_name_to_file() -> None:
    """
    Create a file and write a name into it.
    """

    with open("student.txt", "w", encoding="utf-8") as file:
        file.write("Garv Chouhan")

    print("Data written successfully.")


if __name__ == "__main__":
    write_name_to_file()