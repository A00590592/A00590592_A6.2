import unittest
from source.customer import Customer


class TestCustomer(unittest.TestCase):

    def test_create_customer_valid(self):
        customer = Customer(1, "Alice", "alice@example.com")
        self.assertEqual(customer.customer_id, 1)
        self.assertEqual(customer.name, "Alice")
        self.assertEqual(customer.email, "alice@example.com")

    def test_to_dict(self):
        customer = Customer(2, "Bob", "bob@example.com")
        data = customer.to_dict()
        self.assertEqual(data["customer_id"], 2)
        self.assertEqual(data["name"], "Bob")
        self.assertEqual(data["email"], "bob@example.com")


if __name__ == "__main__":
    unittest.main()