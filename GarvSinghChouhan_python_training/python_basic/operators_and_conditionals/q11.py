""" Check whether a year is a leap year """


def check_leap_year() -> None:
    """
    Check if the given year is leap year
    """
    year = int(input("Enter a year: "))

   # leap year is divisible by 400
   # or it is divisible by 4 but not by 100
    if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
        print("leap year")
    else:
        print("not a leap year")


if __name__ == "__main__":
    check_leap_year()