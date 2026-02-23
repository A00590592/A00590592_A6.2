import os
import tempfile
import unittest

from source.reservation import (
    Reservation,
    load_reservations_from_file,
    save_reservations_to_file,
)


class TestReservation(unittest.TestCase):

    def test_create_reservation_valid(self):
        r = Reservation(
            reservation_id=1,
            hotel_id=10,
            customer_id=20,
            start_date="2026-01-01",
            end_date="2026-01-03",
            rooms_reserved=2,
        )
        self.assertEqual(r.reservation_id, 1)
        self.assertEqual(r.rooms_reserved, 2)

    def test_create_reservation_invalid_rooms(self):
        with self.assertRaises(ValueError):
            Reservation(
                reservation_id=1,
                hotel_id=10,
                customer_id=20,
                start_date="2026-01-01",
                end_date="2026-01-03",
                rooms_reserved=0,
            )

    def test_create_reservation_missing_dates(self):
        with self.assertRaises(ValueError):
            Reservation(
                reservation_id=1,
                hotel_id=10,
                customer_id=20,
                start_date="",
                end_date="2026-01-03",
                rooms_reserved=1,
            )

    def test_to_dict_and_from_dict(self):
        r1 = Reservation(
            reservation_id=5,
            hotel_id=1,
            customer_id=2,
            start_date="2026-02-01",
            end_date="2026-02-02",
            rooms_reserved=1,
        )
        data = r1.to_dict()
        r2 = Reservation.from_dict(data)
        self.assertEqual(r2.reservation_id, 5)
        self.assertEqual(r2.hotel_id, 1)
        self.assertEqual(r2.customer_id, 2)
        self.assertEqual(r2.start_date, "2026-02-01")
        self.assertEqual(r2.end_date, "2026-02-02")
        self.assertEqual(r2.rooms_reserved, 1)

    def test_load_reservations_file_not_found(self):
        reservations = load_reservations_from_file("this_file_does_not_exist_67890.json")
        self.assertEqual(reservations, [])

    def test_save_and_load_reservations(self):
        reservations_in = [
            Reservation(1, 10, 20, "2026-01-01", "2026-01-02", 1),
            Reservation(2, 11, 21, "2026-03-01", "2026-03-03", 2),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "reservations.json")
            save_reservations_to_file(reservations_in, path)

            reservations_out = load_reservations_from_file(path)
            self.assertEqual(len(reservations_out), 2)
            self.assertEqual(reservations_out[0].reservation_id, 1)
            self.assertEqual(reservations_out[1].rooms_reserved, 2)


if __name__ == "__main__":
    unittest.main()