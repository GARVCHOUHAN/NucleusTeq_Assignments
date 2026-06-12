"""
Program to count character frequency.
"""


def count_character_frequency() -> None:
    """
    Count frequency of each character.
    """

    input_string: str = "johnsnowrobstark"

    character_frequency: dict[str, int] = {}

    for character in input_string:
        if character in character_frequency:
            character_frequency[character] += 1
        else:
            character_frequency[character] = 1

    print(character_frequency)


if __name__ == "__main__":
    count_character_frequency()