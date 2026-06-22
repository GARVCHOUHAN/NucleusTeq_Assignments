import re

#1 Write a program to extract all numbers from a given string using regular expressions.
def extract_numbers() -> None:
    """
    Extract all numbers from a string.
    """
    text = "My age is 21 and my marks are 95 and 88."

    numbers = re.findall(r"\d+", text)

    print(numbers)

#2 Write a regular expression to validate an email address.
def validate_email() -> None:
    """
    Validate email address.
    """
    email = "garv@gmail.com"

    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    if re.match(pattern, email):
        print("Valid Email")
    else:
        print("Invalid Email")

#3 Write a regular expression to validate a 10-digit mobile number.
def validate_mobile_number() -> None:
    """
    Validate 10-digit mobile number.
    """
    mobile_number = "9876543210"

    pattern = r"^[0-9]{10}$"

    if re.match(pattern, mobile_number):
        print("Valid Mobile Number")
    else:
        print("Invalid Mobile Number")


#4 Use re.search() to check whether a word exists in a sentence.
def search_word() -> None:
    """
    Check whether a word exists in a sentence.
    """
    sentence = "Python is a powerful programming language"

    result = re.search(r"powerful", sentence)

    if result:
        print("Word Found")
    else:
        print("Word Not Found")


#5 Use re.findall() to extract all words starting with a capital letter.
def extract_capital_words() -> None:
    """
    Extract words starting with capital letters.
    """
    sentence = "Garv Studies Python At SGSITS Indore"

    words = re.findall(r"\b[A-Z][a-zA-Z]*\b", sentence)

    print(words)


#6 Replace multiple spaces in a string with a single space using re.sub().
def replace_multiple_spaces() -> None:
    """
    Replace multiple spaces with single space.
    """
    sentence = "Python     is      easy       to      learn"

    cleaned_sentence = re.sub(r"\s+"," ",sentence)

    print(cleaned_sentence)

#7 Write a pattern to check if a string contains only alphabets.
def validate_alphabets_only() -> None:
    """
    Check whether string contains only alphabets.
    """
    text = "GarvChouhan"

    pattern = r"^[A-Za-z]+$"

    if re.match(pattern, text):
        print("Only Alphabets")
    else:
        print("Contains Other Characters")


#8 Create a password validation program using regex (minimum length, one digit, one special character).
def validate_password() -> None:
    """
    Validate password using regex.
    Conditions:
    - Minimum 8 characters
    - At least one digit
    - At least one special character
    """
    password = "Garv@123"

    pattern = (
        r"^(?=.*[0-9])"
        r"(?=.*[@$!%*?&])"
        r"[A-Za-z0-9@$!%*?&]{8,}$"
        )

    if re.match(pattern, password):
        print("Valid Password")
    else:
        print("Invalid Password")


def main() -> None:
    """
    Execute all regex examples.
    """

    print("\nQuestion 1")
    extract_numbers()

    print("\nQuestion 2")
    validate_email()

    print("\nQuestion 3")
    validate_mobile_number()

    print("\nQuestion 4")
    search_word()

    print("\nQuestion 5")
    extract_capital_words()

    print("\nQuestion 6")
    replace_multiple_spaces()

    print("\nQuestion 7")
    validate_alphabets_only()

    print("\nQuestion 8")
    validate_password()


if __name__ == "__main__":
    main()