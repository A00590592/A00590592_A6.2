"""
Hotel module.

Defines the Hotel class and its core behavior
for the Reservation System A6.2 project.
"""

from datetime import date, datetime
from typing import Dict


class Hotel:
    """Represents a hotel entity."""

    def __init__(self, hotel_id: int, name: str,
                 location: str, total_rooms: int):
        """
        Initialize a hotel.
        """
        if total_rooms <= 0:
            raise ValueError("No rooms available.")

        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.available_rooms = total_rooms

        # Calendar structure: {"YYYY-DOY": rooms_booked}
        self._calendar: Dict[str, int] = {}

    def display_information(self) -> dict:
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "available_rooms": self.available_rooms
        }

    def modify_information(self, name: str = None,
                           location: str = None) -> None:
        if name is not None:
            self.name = name
        if location is not None:
            self.location = location

    def reserve_room(self) -> None:
        if self.available_rooms <= 0:
            raise ValueError("No rooms available.")
        self.available_rooms -= 1

    def cancel_reservation(self) -> None:
        if self.available_rooms >= self.total_rooms:
            raise ValueError("All rooms are already available.")
        self.available_rooms += 1

    @staticmethod
    def _parse_date(value: str) -> date:
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError as exc:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.") from exc

    @staticmethod
    def _calendar_key(day: date) -> str:
        doy = day.timetuple().tm_yday
        return f"{day.year}-{doy:03d}"