
from functools import reduce
from typing import List


#1 Write a lambda function to find the square of a number.
def lambda_square() -> None:
    """
    Lambda function to find square of a number.
    """
    square = lambda number: number ** 2

    print(square(5))

#2 Use map() to convert a list of numbers into their squares.
def map_squares() -> None:
    """
    Use map() to convert numbers into squares.
    """
    numbers = [1, 2, 3, 4, 5]

    squared_numbers = list(map(lambda number: number ** 2, numbers))
    print(squared_numbers)

#3 Use filter() to extract even numbers from a list.
def filter_even_numbers() -> None:
    """
    Use filter() to extract even numbers.
    """
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]

    even_numbers = list(filter(lambda number: number % 2 == 0, numbers))

    print(even_numbers)


#4 Use reduce() to find the product of all elements in a list.
def reduce_product() -> None:
    """
    Use reduce() to find product of all elements.
    """
    numbers = [1, 2, 3, 4, 5]

    product = reduce(lambda first, second: first * second,numbers)

    print(product)


#5 Write a recursive function to calculate factorial.
def factorial(number: int) -> int:
    """
    Recursive factorial function.
    """
    if number == 0 or number == 1:
        return 1

    return number * factorial(number - 1)


#6 Write a recursive function to calculate Fibonacci.
def fibonacci(number: int) -> int:
    """
    Recursive Fibonacci function.
    """
    if number <= 1:
        return number

    return fibonacci(number - 1) + fibonacci(number - 2)


#7 Convert a simple  loop-based program into a functional style using map or filter.
def loop_to_functional() -> None:
    """
    Convert loop-based program into functional style.
    """

    numbers = [1, 2, 3, 4, 5, 6]

    squared_even_numbers = list(
        map(
            lambda number: number ** 2,
            filter(lambda number: number % 2 == 0,numbers)
        )
    )

    print(squared_even_numbers)


def main() -> None:
    """
    Execute all functional programming examples.
    """

    print("\nQuestion 1")
    lambda_square()

    print("\nQuestion 2")
    map_squares()

    print("\nQuestion 3")
    filter_even_numbers()

    print("\nQuestion 4")
    reduce_product()

    print("\nQuestion 5")
    print(factorial(5))

    print("\nQuestion 6")
    print(fibonacci(10))

    print("\nQuestion 7")
    loop_to_functional()


if __name__ == "__main__":
    main()