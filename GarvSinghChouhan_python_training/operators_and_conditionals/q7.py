"""Program to check even or odd number."""


def check_even_or_odd(number: int) -> str:
    """Return Even or Odd."""
    return "Even" if number % 2 == 0 else "Odd"


if __name__ == "__main__":
    print(check_even_or_odd(12))