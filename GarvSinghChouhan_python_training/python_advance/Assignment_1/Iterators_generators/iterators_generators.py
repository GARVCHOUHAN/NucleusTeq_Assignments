
from typing import Iterator


#1 Create an iterator for a list and print elements using next().
def iterator_for_list() -> None:
    """
    Create an iterator for a list and print elements using next().
    """
    numbers = [10, 20, 30, 40, 50]
    iterator = iter(numbers)

    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))
    print(next(iterator))

#2 Write a custom iterator class that returns numbers from 1 to N.
class NumberIterator:
    """
    Custom iterator that returns numbers from 1 to N.
    """

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.current = 1

    def __iter__(self) -> "NumberIterator":
        return self

    def __next__(self) -> int:
        if self.current <= self.limit:
            value = self.current
            self.current += 1
            return value

        raise StopIteration


#3 Write a generator function that yields square numbers up to N.
def square_generator(limit: int) -> Iterator[int]:
    """
    Yield square numbers up to N.
    """
    for number in range(1, limit + 1):
        yield number ** 2


#4 Write a generator to produce Fibonacci numbers.
def fibonacci_generator(limit: int) -> Iterator[int]:
    """
    Generate Fibonacci numbers.
    """
    first_number = 0
    second_number = 1

    for _ in range(limit):
        yield first_number
        first_number, second_number = second_number, first_number + second_number


#5 Write a generator expression to generate even numbers from 1 to 50.
def even_generator_expression() -> None:
    """
    Generate even numbers from 1 to 50.
    """
    even_numbers = (number for number in range(1, 51) if number % 2 == 0)

    for number in even_numbers:
        print(number, end=" ")

    print()


#6 Explain the difference between iterator and generator with a small example.
def iterator_vs_generator() -> None:
    """
    Difference between iterator and generator.
    """

    print("Iterator Example")

    numbers = [1, 2, 3]
    iterator = iter(numbers)

    print(next(iterator))
    print(next(iterator))
    print(next(iterator))

    print("\nGenerator Example")

    def sample_generator() -> Iterator[int]:
        yield 1
        yield 2
        yield 3

    generator = sample_generator()

    print(next(generator))
    print(next(generator))
    print(next(generator))


#7 Write a program that processes a large dataset using a generator instead of storing all values in a list.
def large_dataset_generator(limit: int) -> Iterator[int]:
    """ Process large dataset using generator. """
    for number in range(limit):
        yield number * number

#8 Show an example of a built-in generator (like range) and iterate over it.
def built_in_generator_example() -> None:
    """
    Demonstrate built-in iterable.
    """
    for number in range(1, 11):
        print(number, end=" ")

    print()


def main() -> None:
    """
    Execute all iterator and generator examples.
    """

    print("\nQuestion 1")
    iterator_for_list()

    print("\nQuestion 2")
    custom_iterator = NumberIterator(5)

    for number in custom_iterator:
        print(number)

    print("\nQuestion 3")
    for square in square_generator(5):
        
        print(square)

    print("\nQuestion 4")
    for fibonacci_number in fibonacci_generator(10):
        print(fibonacci_number)

    print("\nQuestion 5")
    even_generator_expression()

    print("\nQuestion 6")
    iterator_vs_generator()

    print("\nQuestion 7")
    for value in large_dataset_generator(10):
        print(value)

    print("\nQuestion 8")
    built_in_generator_example()


if __name__ == "__main__":
    main()