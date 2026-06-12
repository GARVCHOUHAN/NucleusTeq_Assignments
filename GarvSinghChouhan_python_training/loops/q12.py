""" Print numbers from 1 to 100 using loop """


def print_numbers() -> None:
    """
    Print numbers from 1 to 100
    """
    # loop starts from 1 and stops just before 101
    for number in range(1, 101):
        print(number)


if __name__ == "__main__":
    print_numbers()