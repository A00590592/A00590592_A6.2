import unittest
from source.hotel import Hotel


class TestHotel(unittest.TestCase):

    def test_create_valid_hotel(self):
        hotel = Hotel(1, "Test", "MTY", 10)
        self.assertEqual(hotel.hotel_id, 1)
        self.assertEqual(hotel.total_rooms, 10)

    def test_create_invalid_hotel(self):
        with self.assertRaises(ValueError):
            Hotel(1, "Test", "MTY", 0)

    def test_modify_information(self):
        hotel = Hotel(1, "Test", "MTY", 10)
        hotel.modify_information(name="New Name")
        self.assertEqual(hotel.name, "New Name")

    def test_available_rooms_valid(self):
        hotel = Hotel(1, "Test", "MTY", 5)
        self.assertTrue(
            hotel.available_rooms_for_dates("2026-01-01", "2026-01-03", 2)
        )

    def test_available_rooms_invalid_range(self):
        hotel = Hotel(1, "Test", "MTY", 5)
        with self.assertRaises(ValueError):
            hotel.available_rooms_for_dates("2026-01-05", "2026-01-01", 1)


if __name__ == "__main__":
    unittest.main()