""" Print the multiplication table of a number """


def print_multiplication_table() -> None:
    """
    Print the multiplication table of a number entered by user
    """
    num = int(input("Enter a number: "))

    for count in range(1, 11):
        print(f"{num} x {count} = {num * count}")


if __name__ == "__main__":
    print_multiplication_table()