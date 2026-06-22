"""
Exception Handling Assignment Solutions.

This module demonstrates:

1. ValueError handling
2. ZeroDivisionError handling
3. try-except-else-finally
4. Multiple exception handling
5. Catching all exceptions
6. Raising ValueError manually
7. Custom exception handling
8. FileNotFoundError handling
"""

from typing import Any

from numpy import number


MINIMUM_AGE = 18


class AgeException(Exception):
    """
    Custom exception raised when age is less than 18.
    """

# 1. ValueError handling
def handle_invalid_integer() -> None:
    """
    Take a number as input and handle ValueError.
    """
    try:
        number = int(input("Enter an integer: "))
        print(f"Entered number: {number}")

    except ValueError:
        print("Error: Invalid integer entered.")


# 2. ZeroDivisionError handling
def divide_numbers() -> None:
    """
    Divide two numbers and handle ZeroDivisionError.
    """
    try:
        first_number = float(input("Enter first number: "))
        second_number = float(input("Enter second number: "))

        result = first_number / second_number

        print(f"Result: {result}")

    except ZeroDivisionError:
        print("Error: Division by zero is not allowed.")
        

#3  Write a program using try-except-else-finally to read a number from a file  and print its square. 
def read_number_and_print_square(
    file_name: str
) -> None:
    """
    Read a number from file and print its square.
    Demonstrates try-except-else-finally.
    """
    try:
        with open(
            file_name,
            "r",
            encoding="utf-8"
        ) as file:
            number = int(file.read())

    except FileNotFoundError:
        print("Error: File not found.")

    except ValueError:
        print("Error: File does not contain a valid integer.")

    else:
        print( f"Square of {number} is {number ** 2}")

    finally:
        print("File operation completed.")


#4 Handle multiple exceptions  in a single program.
def handle_multiple_exceptions(
    file_name: str,
    divisor: int
) -> None:
    """
    Handle multiple exceptions in a single program.
    """
    try:
        with open(
            file_name,
            "r",
            encoding="utf-8"
        ) as file:
            value = int(file.read())

        result = value / divisor

        print(f"Result: {result}")

    except FileNotFoundError:
        print("Error: File not found.")

    except ValueError:
        print("Error: Invalid integer inside file.")

    except ZeroDivisionError:
        print("Error: Division by zero attempted.")

#5 Write a program that catches all exceptions and prints the error message.
def catch_all_exceptions() -> None:
    """
    Catch all exceptions and print error message.
    """
    try:
        number = int("hello")
        print(number)

    except Exception as error:
        print(f"Exception occurred: {error}")


#6 Create a function that raises a ValueError if a number is negative.
def validate_positive_number(
    number: int
) -> None:
    """
    Raise ValueError if number is negative.
    """
    if number < 0:
        raise ValueError(
            "Negative numbers are not allowed."
        )

    print("Valid positive number.")


#7 Create a custom exception called AgeException and raise it if age is less than 18.
def validate_age(age: int) -> None:
    """
    Raise AgeException if age is less than 18.
    """
    if age < MINIMUM_AGE:
        raise AgeException(f"Age must be at least {MINIMUM_AGE}.")

    print("Age is valid.")


#8 Write a program that handles FileNotFoundError when trying to open a file.
def open_file(file_name: str) -> None:
    """
    Handle FileNotFoundError while opening a file.
    """
    try:
        with open(
            file_name,
            "r",
            encoding="utf-8"
        ) as file:
            print(file.read())

    except FileNotFoundError:
        print(
            "Error: Requested file does not exist."
        )


def main() -> None:
    """
    Execute all exception handling examples.
    """

    print(
        "\nQuestion 1: ValueError Handling"
    )
    handle_invalid_integer()

    print(
        "\nQuestion 2: ZeroDivisionError Handling"
    )
    divide_numbers()

    print(
        "\nQuestion 3: try-except-else-finally"
    )
    read_number_and_print_square("number.txt")

    print(
        "\nQuestion 4: Multiple Exceptions"
    )
    handle_multiple_exceptions(
        "number.txt",
        2
    )

    print(
        "\nQuestion 5: Catch All Exceptions"
    )
    catch_all_exceptions()

    print(
        "\nQuestion 6: Raise ValueError"
    )
    try:
        validate_positive_number(-10)

    except ValueError as error:
        print(error)

    print(
        "\nQuestion 7: Custom Exception"
    )
    try:
        validate_age(16)

    except AgeException as error:
        print(error)

    print(
        "\nQuestion 8: FileNotFoundError"
    )
    open_file("sample.txt")


if __name__ == "__main__":
    main()