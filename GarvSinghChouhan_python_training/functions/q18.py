""" Check whether a number or string is a palindrome or not"""


def is_palindrome(value: str) -> bool:
    """
    Return True if input is palindrome otherwise False
    """
    # convert value to string and compare it with its reversed value
    value = str(value)
    return value == value[::-1]


if __name__ == "__main__":
    value = input("Enter a number or string : ")
    if is_palindrome(value):
        print(value, "is a palindrome")
    else:
        print(value, "is not a palindrome")
        