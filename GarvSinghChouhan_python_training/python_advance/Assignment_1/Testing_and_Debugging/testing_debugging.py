import pdb


#1 Write pytest test cases for a function that adds two numbers.
def add_numbers(first_number: int, second_number: int) -> int:
    """
    Add two numbers.
    """
    return first_number + second_number


#2 Write pytest test cases for a function that checks whether a number is prime.
def is_prime(number: int) -> bool:
    """
    Check whether a number is prime.
    """
    if number <= 1:
        return False

    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False

    return True


#3 Create a function with a logical bug and use pdb to identify the issue.
def buggy_average(numbers: list[int]) -> float:
    """
    Function containing a logical bug.
    """

    total = 0

    for number in numbers:
        total += number

    pdb.set_trace()

    return total // len(numbers)


#4 Use pdb breakpoints inside a loop and inspect variable values.
def loop_debugging() -> None:
    """
    Demonstrate pdb inside a loop.
    """

    for number in range(1, 6):
        pdb.set_trace()
        square = number ** 2
        print(square)


#5 Explain the advantages of using an IDE debugger over print statements.
def explain_ide_debugger() -> None:
    """
    Advantages of IDE debugger.
    """

    advantages = [
        "Step-by-step execution",
        "Variable inspection",
        "Breakpoint support",
        "Call stack analysis",
        "Faster bug detection",
        "No need for multiple print statements"
    ]

    for advantage in advantages:
        print(advantage)


def main() -> None:

    print("\nAddition Function")
    print(add_numbers(10, 20))

    print("\nPrime Function")
    print(is_prime(11))

    print("\nBuggy Function")
    print(buggy_average([10, 20, 30]))

    print("\nLoop Debugging")
    loop_debugging()

    print("\nIDE Debugger Advantages")
    explain_ide_debugger()


if __name__ == "__main__":
    main()