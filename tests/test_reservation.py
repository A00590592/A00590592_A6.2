import unittest
from source.reservation import Reservation


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


if __name__ == "__main__":
    unittest.main()