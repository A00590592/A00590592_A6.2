"""
Reservation module.
"""

import json
from typing import List


class Reservation:
    def __init__(
        self,
        reservation_id: int,
        hotel_id: int,
        customer_id: int,
        start_date: str,
        end_date: str,
        rooms_reserved: int,
    ):
        if rooms_reserved <= 0:
            raise ValueError("Rooms reserved must be at least 1.")
        if not start_date or not end_date:
            raise ValueError("Start and end dates are required.")

        self.reservation_id = reservation_id
        self.hotel_id = hotel_id
        self.customer_id = customer_id
        self.start_date = start_date
        self.end_date = end_date
        self.rooms_reserved = rooms_reserved

    def to_dict(self) -> dict:
        return {
            "reservation_id": self.reservation_id,
            "hotel_id": self.hotel_id,
            "customer_id": self.customer_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "rooms_reserved": self.rooms_reserved,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Reservation":
        return cls(
            reservation_id=int(data["reservation_id"]),
            hotel_id=int(data["hotel_id"]),
            customer_id=int(data["customer_id"]),
            start_date=str(data["start_date"]),
            end_date=str(data["end_date"]),
            rooms_reserved=int(data["rooms_reserved"]),
        )


def save_reservations_to_file(reservations: List[Reservation], file_path: str) -> None:
    data = [r.to_dict() for r in reservations]
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def load_reservations_from_file(file_path: str) -> List[Reservation]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    return [Reservation.from_dict(item) for item in data]