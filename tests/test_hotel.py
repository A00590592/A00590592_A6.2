import os
import tempfile
import unittest

from source.hotel import Hotel, load_hotels_from_file


class TestHotel(unittest.TestCase):

    def test_create_valid_hotel(self):
        hotel = Hotel(1, "Test", "MTY", 10)
        self.assertEqual(hotel.hotel_id, 1)
        self.assertEqual(hotel.total_rooms, 10)

    def test_create_invalid_hotel(self):
        with self.assertRaises(ValueError):
            Hotel(1, "Test", "MTY", 0)

    def test_create_hotel_empty_name(self):
        with self.assertRaises(ValueError):
            Hotel(1, "", "MTY", 10)

    def test_create_hotel_empty_location(self):
        with self.assertRaises(ValueError):
            Hotel(1, "Test", "", 10)

    def test_modify_information(self):
        hotel = Hotel(1, "Test", "MTY", 10)
        hotel.modify_information(name="New Name")
        self.assertEqual(hotel.name, "New Name")

    def test_modify_information_empty_name_raises(self):
        hotel = Hotel(1, "Test", "MTY", 10)
        with self.assertRaises(ValueError):
            hotel.modify_information(name="")

    def test_modify_information_empty_location_raises(self):
        hotel = Hotel(1, "Test", "MTY", 10)
        with self.assertRaises(ValueError):
            hotel.modify_information(location="")

    def test_available_rooms_valid(self):
        hotel = Hotel(1, "Test", "MTY", 5)
        self.assertTrue(
            hotel.available_rooms_for_dates("2026-01-01", "2026-01-03", 2)
        )

    def test_available_rooms_invalid_range(self):
        hotel = Hotel(1, "Test", "MTY", 5)
        with self.assertRaises(ValueError):
            hotel.available_rooms_for_dates("2026-01-05", "2026-01-01", 1)

    def test_available_rooms_invalid_rooms_requested(self):
        hotel = Hotel(1, "Test", "MTY", 5)
        with self.assertRaises(ValueError):
            hotel.available_rooms_for_dates("2026-01-01", "2026-01-03", 0)

    def test_invalid_date_format(self):
        hotel = Hotel(1, "Test", "MTY", 5)
        with self.assertRaises(ValueError):
            hotel.available_rooms_for_dates("bad-date", "2026-01-03", 1)

    def test_reserve_and_cancel_room(self):
        hotel = Hotel(1, "Test", "MTY", 2)
        hotel.reserve_room()
        self.assertEqual(hotel.available_rooms, 1)
        hotel.cancel_reservation()
        self.assertEqual(hotel.available_rooms, 2)

    def test_load_hotels_invalid_json_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "hotels.json")
            with open(path, "w", encoding="utf-8") as file:
                file.write("{invalid json")

            hotels = load_hotels_from_file(path)
            self.assertEqual(hotels, [])


if __name__ == "__main__":
    unittest.main()