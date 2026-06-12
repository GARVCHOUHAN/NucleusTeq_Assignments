""" Find the largest of three numbers """


def find_largest_number() -> None:
    """
    Find the largest number entered by the user
    """
    first_number = float(input("Enter first number: "))
    second_number = float(input("Enter second number: "))
    third_number = float(input("Enter third number: "))

    # comparing each number with the other two numbers to find the largest one
    if first_number >= second_number and first_number >= third_number:
        print("largest number: ", first_number)
    elif second_number >= first_number and second_number >= third_number:
        print("largest number: ", second_number)
    else:
        print("largest number: ", third_number)


if __name__ == "__main__":
    find_largest_number()