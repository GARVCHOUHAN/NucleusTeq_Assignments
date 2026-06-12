""" 
Create variables of type int, float, string and boolean
Print their types using type() 
"""

def print_variable_types() -> None: 
    """                                                         
    Create variables and display their data types
    """
    integer_value = 100
    float_value = 12.45
    string_value = "Garv Singh Chouhan"
    boolean_value = False

    # displaying data types of variable 
    print(type(integer_value))
    print(type(float_value))
    print(type(string_value))
    print(type(boolean_value))


if __name__ == "__main__":
    print_variable_types()