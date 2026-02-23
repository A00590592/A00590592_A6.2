import os
import tempfile
import unittest

from source.customer import (
    Customer,
    load_customers_from_file,
    save_customers_to_file,
)


class TestCustomer(unittest.TestCase):

    def test_create_customer_valid(self):
        customer = Customer(1, "Alice", "alice@example.com")
        self.assertEqual(customer.customer_id, 1)
        self.assertEqual(customer.name, "Alice")
        self.assertEqual(customer.email, "alice@example.com")

    def test_create_customer_invalid_name(self):
        with self.assertRaises(ValueError):
            Customer(1, "", "a@a.com")

    def test_create_customer_invalid_email(self):
        with self.assertRaises(ValueError):
            Customer(1, "Alice", "")

    def test_to_dict(self):
        customer = Customer(2, "Bob", "bob@example.com")
        data = customer.to_dict()
        self.assertEqual(data["customer_id"], 2)
        self.assertEqual(data["name"], "Bob")
        self.assertEqual(data["email"], "bob@example.com")

    def test_from_dict(self):
        data = {"customer_id": 3, "name": "Carl", "email": "carl@test.com"}
        customer = Customer.from_dict(data)
        self.assertEqual(customer.customer_id, 3)
        self.assertEqual(customer.name, "Carl")
        self.assertEqual(customer.email, "carl@test.com")

    def test_load_customers_file_not_found(self):
        customers = load_customers_from_file("this_file_does_not_exist_12345.json")
        self.assertEqual(customers, [])

    def test_save_and_load_customers(self):
        customers_in = [
            Customer(10, "Ana", "ana@test.com"),
            Customer(11, "Luis", "luis@test.com"),
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "customers.json")
            save_customers_to_file(customers_in, path)

            customers_out = load_customers_from_file(path)
            self.assertEqual(len(customers_out), 2)
            self.assertEqual(customers_out[0].customer_id, 10)
            self.assertEqual(customers_out[1].email, "luis@test.com")


if __name__ == "__main__":
    unittest.main()