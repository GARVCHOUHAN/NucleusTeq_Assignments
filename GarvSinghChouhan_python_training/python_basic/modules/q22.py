""" find square root, power, and factorial using math module """

import math

def perform_math_operations() -> None:
    """
    print square root, power, and factorial
    """
    number = int(input("Enter a number: "))
    power = int(input("Enter the power: "))

    print("Square root:", math.sqrt(number))
    print("Power:", math.pow(number, power))
    print("Factorial:", math.factorial(number))


if __name__ == "__main__":
    perform_math_operations()