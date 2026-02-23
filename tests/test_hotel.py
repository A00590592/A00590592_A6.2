import os
import tempfile
import unittest

from source.hotel import Hotel, load_hotels_from_file, save_hotels_to_file


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

    def test_apply_calendar_change_valid_reserve_and_cancel(self):
        hotel = Hotel(1, "Test", "MTY", 5)
        
        """Reserve 2 rooms."""
        hotel.apply_calendar_change("2026-01-01", "2026-01-02", 2, 1)
        key = hotel._calendar_key(hotel._parse_date("2026-01-01"))
        self.assertEqual(hotel._calendar[key], 2)
        
        """Cancel 1 room."""
        hotel.apply_calendar_change("2026-01-01", "2026-01-02", 1, -1)
        self.assertEqual(hotel._calendar[key], 1)

    def test_apply_calendar_change_invalid_inputs(self):
        hotel = Hotel(1, "Test", "MTY", 5)
        with self.assertRaises(ValueError):
            hotel.apply_calendar_change("2026-01-01", "2026-01-02", 0, 1)
        with self.assertRaises(ValueError):
            hotel.apply_calendar_change("2026-01-01", "2026-01-02", 1, 99)
        with self.assertRaises(ValueError):
            hotel.apply_calendar_change("2026-01-05", "2026-01-01", 1, 1)

    def test_apply_calendar_change_cancel_exceeds_booked(self):
        """Try to cancel when there are no previous reservations."""
        hotel = Hotel(1, "Test", "MTY", 5)
        with self.assertRaises(ValueError):
            hotel.apply_calendar_change("2026-01-01", "2026-01-02", 1, -1)

    def test_available_rooms_not_enough(self):
        hotel = Hotel(1, "Test", "MTY", 5)
        
        """Fill the hotel."""
        hotel.apply_calendar_change("2026-01-01", "2026-01-01", 5, 1)
        
        """Try to request 1 room, should return False."""
        self.assertFalse(hotel.available_rooms_for_dates("2026-01-01", "2026-01-01", 1))

    def test_reserve_room_no_availability(self):
        hotel = Hotel(1, "Test", "MTY", 1)
        hotel.reserve_room()
        with self.assertRaises(ValueError):
            hotel.reserve_room()

    def test_cancel_reservation_all_available(self):
        hotel = Hotel(1, "Test", "MTY", 1)
        with self.assertRaises(ValueError):
            hotel.cancel_reservation()

    def test_display_information(self):
        hotel = Hotel(1, "Test", "MTY", 5)
        info = hotel.display_information()
        self.assertEqual(info["name"], "Test")
        self.assertEqual(info["total_rooms"], 5)

    def test_to_and_from_dict(self):
        hotel = Hotel(1, "Test", "MTY", 5)
        data = hotel.to_dict()
        self.assertEqual(data["location"], "MTY")
        
        hotel2 = Hotel.from_dict(data)
        self.assertEqual(hotel2.hotel_id, 1)
        self.assertEqual(hotel2.name, "Test")

    def test_save_and_load_valid_hotels(self):
        hotel = Hotel(1, "Test", "MTY", 5)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "hotels.json")
            
            """Save the file."""
            save_hotels_to_file([hotel], path)
            self.assertTrue(os.path.exists(path))
            
            """Load it and verify."""
            loaded_hotels = load_hotels_from_file(path)
            self.assertEqual(len(loaded_hotels), 1)
            self.assertEqual(loaded_hotels[0].name, "Test")

    def test_load_hotels_file_not_found(self):
        """Non-existent file should return an empty list."""
        hotels = load_hotels_from_file("fake_path_123.json")
        self.assertEqual(hotels, [])


if __name__ == "__main__":
    unittest.main()