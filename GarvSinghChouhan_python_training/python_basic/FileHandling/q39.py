### Question 39: Search a Word in a File

"""
Program to search for a word in a file.
"""


SEARCH_WORD = "Python"


def search_word_in_file() -> None:
    """
    Search a specific word in a file.
    """

    with open("student.txt", "r", encoding="utf-8") as file:
        content: str = file.read()

    if SEARCH_WORD in content:
        print(f"'{SEARCH_WORD}' found in file.")
    else:
        print(f"'{SEARCH_WORD}' not found in file.")


if __name__ == "__main__":
    search_word_in_file()
