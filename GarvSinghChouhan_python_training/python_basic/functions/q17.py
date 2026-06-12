""" Calculate the square of a number """


def calculate_square(number: int) -> int:
    """
    calculate and return the square of a number
    """
    square = number * number
    return square


if __name__ == "__main__":
    number = int(input("Enter a number: "))
    result = calculate_square(number)
    print("Square: ", result)