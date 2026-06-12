""" Find the factorial of a number """


def find_factorial() -> None:
    """
    calculate and print factorial of a number
    """
    number = int(input("Enter a number: "))

    factorial = 1

    # multipling all numbers from 1 to given number to find its factorial
    for i in range(1, number + 1):
        factorial = factorial * i

    print("Factorial is: ", factorial)


if __name__ == "__main__":
    find_factorial()