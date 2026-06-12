"""
Program demonstrating encapsulation.
"""


class Bank:
    """
    Represents a bank account.
    """

    def __init__(
        self,
        balance: float
    ) -> None:
        self.__balance = balance

    def deposit(
        self,
        amount: float
    ) -> None:
        """
        Deposit money into account.
        """

        self.__balance += amount

    def withdraw(
        self,
        amount: float
    ) -> None:
        """
        Withdraw money from account.
        """

        if amount <= self.__balance:
            self.__balance -= amount
        else:
            print("Insufficient Balance")

    def get_balance(self) -> float:
        """
        Return current account balance.
        """

        return self.__balance


if __name__ == "__main__":
    account = Bank(1000)

    account.deposit(500)
    account.withdraw(200)

    print("Current Balance:", account.get_balance())