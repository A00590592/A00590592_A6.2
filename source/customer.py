"""
Customer module.
"""

import json
from typing import List


class Customer:
    def __init__(self, customer_id: int, name: str, email: str):
        if not name:
            raise ValueError("Customer name cannot be empty.")
        if not email:
            raise ValueError("Customer email cannot be empty.")

        self.customer_id = customer_id
        self.name = name
        self.email = email

    def to_dict(self) -> dict:
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Customer":
        return cls(
            customer_id=int(data["customer_id"]),
            name=str(data["name"]),
            email=str(data["email"]),
        )


def save_customers_to_file(customers: List[Customer], file_path: str) -> None:
    data = [customer.to_dict() for customer in customers]
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def load_customers_from_file(file_path: str) -> List[Customer]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    return [Customer.from_dict(item) for item in data]