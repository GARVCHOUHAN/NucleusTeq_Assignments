""" Reverse a list without using reverse() """


def reverse_list() -> None:
   
    original_list = [10, 20, 30, 40, 50]

    reversed_list = []

    # take last element of original list and add it to reversed list until we reach the first element
    for index in range(len(original_list) - 1, -1, -1):
        reversed_list.append(original_list[index])

    print("Original list:", original_list)
    print("Reversed list:", reversed_list)


if __name__ == "__main__":
    reverse_list()