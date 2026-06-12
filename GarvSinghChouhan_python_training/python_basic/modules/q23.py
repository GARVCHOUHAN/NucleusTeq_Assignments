""" Program to generate random numbers using random module """

import random

def generate_random_numbers():
    """
    Generate and print random numbers between 1 to 100
    """
    print("Random Integer number:", random.randint(1, 100))
    print("Random Float number:", random.random() * 100)


if __name__ == "__main__":
    generate_random_numbers()