""" Program to identify number type. """ 


def check_number_type(number: int) -> str:
    """Check sign of number."""
    if number > 0:
        return "Positive"
    if number < 0:
        return "Negative"
    return "Zero"

if __name__ == "__main__":
    print(check_number_type(-10))