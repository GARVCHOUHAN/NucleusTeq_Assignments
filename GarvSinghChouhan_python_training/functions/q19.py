"""
Question 19 : Write a function that returns maximum number from a list.
"""

def find_maximum(numbers: list[int]) -> int:
    """
    Find the maximum number from a list.
    """
    return max(numbers)

def display_maximum(maximum_number: int) -> None:
    """
    Display the maximum number.
    """

    print(f"The maximum number in the list is: {maximum_number}")
    
if __name__ == "__main__":
    numbers = [10, 25, 8, 40, 15]

    maximum_number = find_maximum(numbers)
    display_maximum(maximum_number)