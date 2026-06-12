"""
Program importing and using a custom module.
"""

from custom_module import is_prime


def execute_prime_check() -> None:
    """
    Execute prime number check.
    """

    number_to_check: int = int(input("Enter a number to check if it is prime: "))

    if is_prime(number_to_check):
        print(f"{number_to_check} is a Prime Number.")
    else:
        print(f"{number_to_check} is Not a Prime Number.")


if __name__ == "__main__":
    execute_prime_check()