###  Read a File and Count Words, Lines, and Characters

"""
Program to count words, lines, and characters in a file.
"""


def count_file_statistics() -> None:
    """
    Read file and display statistics.
    """

    with open("student.txt", "r", encoding="utf-8") as file:
        content: str = file.read()

    word_count: int = len(content.split())
    character_count: int = len(content)

    with open("student.txt", "r", encoding="utf-8") as file:
        line_count: int = len(file.readlines())

    print("Words:", word_count)
    print("Lines:", line_count)
    print("Characters:", character_count)


if __name__ == "__main__":
    count_file_statistics()
