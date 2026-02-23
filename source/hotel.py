"""
Hotel module.

Defines the Hotel class and its core behavior
for the Reservation System A6.2 project.
"""

import json
from datetime import date, datetime, timedelta
from typing import Dict, List


class Hotel:
    """Represents a hotel entity."""

    def __init__(self, hotel_id: int, name: str, location: str, total_rooms: int):
        if not name:
            raise ValueError("Hotel name cannot be empty.")
        if not location:
            raise ValueError("Hotel location cannot be empty.")
        if total_rooms <= 0:
            raise ValueError("No rooms available.")

        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.available_rooms = total_rooms
        self._calendar: Dict[str, int] = {}

    def available_rooms_for_dates(
        self,
        start_date: str,
        end_date: str,
        rooms_requested: int = 1,
    ) -> bool:
        if rooms_requested <= 0:
            raise ValueError("Rooms requested must be at least 1.")

        start = self._parse_date(start_date)
        end = self._parse_date(end_date)

        if start > end:
            raise ValueError("End date must be greater than or equal to start date.")

        current = start
        while current <= end:
            key = self._calendar_key(current)
            booked = self._calendar.get(key, 0)

            if booked + rooms_requested > self.total_rooms:
                return False

            current += timedelta(days=1)

        return True

    def display_information(self) -> dict:
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "available_rooms": self.available_rooms,
        }

    def modify_information(self, name: str = None, location: str = None) -> None:
        if name is not None:
            if not name:
                raise ValueError("Hotel name cannot be empty.")
            self.name = name

        if location is not None:
            if not location:
                raise ValueError("Hotel location cannot be empty.")
            self.location = location

    def reserve_room(self) -> None:
        if self.available_rooms <= 0:
            raise ValueError("No rooms available.")
        self.available_rooms -= 1

    def cancel_reservation(self) -> None:
        if self.available_rooms >= self.total_rooms:
            raise ValueError("All rooms are already available.")
        self.available_rooms += 1

    def to_dict(self) -> dict:
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "total_rooms": self.total_rooms,
            "available_rooms": self.available_rooms,
            "calendar": self._calendar,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Hotel":
        hotel = cls(
            hotel_id=int(data["hotel_id"]),
            name=str(data["name"]),
            location=str(data["location"]),
            total_rooms=int(data["total_rooms"]),
        )
        hotel.available_rooms = int(data.get("available_rooms", hotel.total_rooms))
        hotel._calendar = dict(data.get("calendar", {}))
        return hotel

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


def save_hotels_to_file(hotels: List[Hotel], file_path: str) -> None:
    data = [hotel.to_dict() for hotel in hotels]
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def load_hotels_from_file(file_path: str) -> List[Hotel]:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    return [Hotel.from_dict(item) for item in data]