""" Count even and odd numbers in a list """


def count_even_and_odd_numbers() -> None:
   
    list = [11, 78, 85, 96, 56, 73, 53, 56, 55]

    even_count = 0
    odd_count = 0

    # even number leaves remainder 0 when divided by 2
    for number in list:
        if number % 2 == 0:
            even_count += 1
        else:
            odd_count += 1

    print("list:", list)
    print("Even numbers:", even_count)
    print("Odd numbers:", odd_count)


if __name__ == "__main__":
    count_even_and_odd_numbers()