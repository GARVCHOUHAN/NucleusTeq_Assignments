""" Check whether a number is prime """


def check_prime_number() -> None:
    """
    Check if a number is prime or not
    """
    number = int(input("Enter a number: "))

    if number <= 1:
        print(f"{number} is not a prime number")
        return

    # prime number is divisible only by 1 and itself
    for i in range(2, number):
        if number % i == 0:
            print("not a prime number")
            return
    print("prime number")


if __name__ == "__main__":
    check_prime_number()