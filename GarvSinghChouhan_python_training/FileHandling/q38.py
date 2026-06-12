### Question 38: Copy Content from One File to Another

"""
Program to copy contents of one file into another.
"""


def copy_file_content() -> None:
    """
    Copy source file content to destination file.
    """

    with open("student.txt", "r", encoding="utf-8") as source_file:
        content: str = source_file.read()

    with open("backup.txt", "w", encoding="utf-8") as destination_file:
        destination_file.write(content)

    print("File copied successfully.")


if __name__ == "__main__":
    copy_file_content()
