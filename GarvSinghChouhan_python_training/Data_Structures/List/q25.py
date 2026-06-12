""" Perform operations on a list of numbers """


def list_operations() -> None:
    """
    Find sum, maximum value, sort the list, and remove duplicates
    """
    numbers = [10,56, 74, 78, 8, 9, 85, 466, 49]

    print("Original list:", numbers)

    # sum
    print("Sum:", sum(numbers))

    # max
    print("Maximum number:", max(numbers))

    # Sort
    print("Sorted list:", sorted(numbers))

    # removes duplicates
    # set removes duplicates and then convert back to list
    unique_numbers = list(set(numbers))      
    print("List without duplicates:", unique_numbers)


if __name__ == "__main__":
    list_operations()