""" Reverse a number using a loop """


def reverse_number() -> None:
    """
    Reverse the digits of a number
    """
    number = int(input("Enter a number: "))

    reversed_number = 0

    # taking the last digit of a number and add it to reversed number until the number becomes 0
    while number > 0:
        last_digit = number % 10
        reversed_number = reversed_number * 10 + last_digit
        number = number // 10

    print("Reversed number: ", reversed_number)


if __name__ == "__main__":
    reverse_number()