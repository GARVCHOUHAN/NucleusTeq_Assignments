""" a function using default parameters."""

def default_msg(name:str = "User") -> None:
    """
    Display a greeting message.
    """
    print(f"Welcome, {name}!")

if __name__ == "__main__":
    default_msg()  # Using default parameter
    default_msg("Neymar Jr")  # Providing a custom name