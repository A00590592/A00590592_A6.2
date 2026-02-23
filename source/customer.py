"""
Customer module.

Provides the Customer class and helper functions to persist customers in JSON files.
"""

# pylint: disable=duplicate-code


import json
from typing import List


class Customer:
    """Represents a customer entity."""

    def __init__(self, customer_id: int, name: str, email: str):
        """Initialize a customer."""
        if not name:
            raise ValueError("Customer name cannot be empty.")
        if not email:
            raise ValueError("Customer email cannot be empty.")

        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self) -> dict:
        """Return a JSON-serializable representation of the customer."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Customer":
        """Create a Customer instance from a dictionary."""
        return cls(
            customer_id=int(data["customer_id"]),
            name=str(data["name"]),
            email=str(data["email"]),
        )


def save_customers_to_file(customers: List[Customer], file_path: str) -> None:
    """Save a list of customers to a JSON file."""
    data = [customer.to_dict() for customer in customers]
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def load_customers_from_file(file_path: str) -> List[Customer]:
    """Load customers from a JSON file. Returns an empty list if the file is missing."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    return [Customer.from_dict(item) for item in data]
