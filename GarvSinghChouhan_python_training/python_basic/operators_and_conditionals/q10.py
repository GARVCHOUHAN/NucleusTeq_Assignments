""" Calculation of grade based on marks """


def calculate_grade() -> None:
    """
    Calculate grade from the marks entered by the user
    """
    marks = float(input("Enter marks: "))

    # comparing the marks and assigning a grade
    if marks >= 80:
        print("Grade A")
    elif marks >= 60:
        print("Grade B")
    elif marks >= 40:
        print("Grade C")
    else:
        print("Fail")


if __name__ == "__main__":
    calculate_grade()