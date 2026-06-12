""" Program to swap two numbers """


def swap_numbers() -> None:
    """
    Taking two numbers as input and swap their values
    """
    first_number = int(input("Enter first number: "))
    second_number = int(input("Enter second number: "))

    print("Before swapping:")
    print(f"First number: {first_number}, Second number: {second_number}")

    # swapping the values of both numbers
    first_number, second_number = second_number, first_number

    print("After swapping:")
    print(f"First number: {first_number}, Second number: {second_number}")


if __name__ == "__main__":
    swap_numbers()