"""
Program demonstrating constructor usage.
"""


class Car:
    """
    Represents a car object.
    """

    def __init__(
        self,
        brand: str,
        model: str
    ) -> None:
        """
        Initialize car attributes.
        """

        self.brand = brand
        self.model = model

    def display_car_details(self) -> None:
        """
        Display car information.
        """

        print("Brand:", self.brand)
        print("Model:", self.model)


if __name__ == "__main__":
    car = Car(
        "Hyundai",
        "Verna"
    )

    car.display_car_details()