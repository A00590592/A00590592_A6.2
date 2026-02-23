from datetime import timedelta

from customer import Customer, load_customers_from_file, save_customers_to_file
from hotel import Hotel, load_hotels_from_file, save_hotels_to_file


HOTELS_FILE = "hotels.json"
CUSTOMERS_FILE = "customers.json"


class CancelOperation(Exception):
    pass


def prompt_input(message: str) -> str:
    value = input(message).strip()
    if value.lower() == "cancel":
        raise CancelOperation()
    return value


def prompt_int(message: str) -> int:
    value = prompt_input(message)
    return int(value)


def pause() -> None:
    input("\nPress Enter to return to the main menu...")


def find_hotel(hotels: list, hotel_id: int):
    for hotel in hotels:
        if hotel.hotel_id == hotel_id:
            return hotel
    return None


def find_customer(customers: list, customer_id: int):
    for customer in customers:
        if customer.customer_id == customer_id:
            return customer
    return None


def create_hotel(hotels: list) -> None:
    print("\nType 'cancel' at any time to return to the main menu.\n")

    hotel_id = prompt_int("Hotel ID: ")
    name = prompt_input("Name: ")
    location = prompt_input("Location: ")
    total_rooms = prompt_int("Total rooms: ")

    if not name:
        raise ValueError("Name cannot be empty.")
    if not location:
        raise ValueError("Location cannot be empty.")
    if find_hotel(hotels, hotel_id) is not None:
        raise ValueError("Hotel ID already exists.")

    hotels.append(Hotel(hotel_id, name, location, total_rooms))
    print("Hotel created.")


def list_hotels(hotels: list) -> None:
    if not hotels:
        print("No hotels found.")
        return

    for hotel in hotels:
        print({
            "hotel_id": hotel.hotel_id,
            "name": hotel.name,
            "location": hotel.location,
            "total_rooms": hotel.total_rooms,
        })


def consult_hotel(hotels: list) -> None:
    print("\nType 'cancel' at any time to return to the main menu.\n")

    hotel_id = prompt_int("Hotel ID: ")
    hotel = find_hotel(hotels, hotel_id)
    if hotel is None:
        raise ValueError("Hotel not found.")
    print(hotel.display_information())


def delete_hotel(hotels: list) -> None:
    print("\nType 'cancel' at any time to return to the main menu.\n")

    hotel_id = prompt_int("Hotel ID to delete: ")
    for idx, hotel in enumerate(hotels):
        if hotel.hotel_id == hotel_id:
            hotels.pop(idx)
            print("Hotel deleted.")
            return
    raise ValueError("Hotel not found.")


def create_customer(customers: list) -> None:
    print("\nType 'cancel' at any time to return to the main menu.\n")

    customer_id = prompt_int("Customer ID: ")
    name = prompt_input("Name: ")
    email = prompt_input("Email: ")

    if find_customer(customers, customer_id) is not None:
        raise ValueError("Customer ID already exists.")

    customers.append(Customer(customer_id, name, email))
    print("Customer created.")


def list_customers(customers: list) -> None:
    if not customers:
        print("No customers found.")
        return
    for customer in customers:
        print(customer.to_dict())


def consult_customer(customers: list) -> None:
    print("\nType 'cancel' at any time to return to the main menu.\n")

    customer_id = prompt_int("Customer ID: ")
    customer = find_customer(customers, customer_id)
    if customer is None:
        raise ValueError("Customer not found.")
    print(customer.to_dict())


def delete_customer(customers: list) -> None:
    print("\nType 'cancel' at any time to return to the main menu.\n")

    customer_id = prompt_int("Customer ID to delete: ")
    for idx, customer in enumerate(customers):
        if customer.customer_id == customer_id:
            customers.pop(idx)
            print("Customer deleted.")
            return
    raise ValueError("Customer not found.")


def apply_calendar_change(hotel: Hotel, start_date: str, end_date: str, rooms: int, sign: int) -> None:
    start = Hotel._parse_date(start_date)
    end = Hotel._parse_date(end_date)

    if start > end:
        raise ValueError("End date must be greater than or equal to start date.")

    current = start
    while current <= end:
        key = Hotel._calendar_key(current)
        booked = hotel._calendar.get(key, 0)
        new_value = booked + (rooms * sign)

        if new_value < 0:
            raise ValueError("Cancellation exceeds booked rooms for selected dates.")

        if new_value == 0:
            hotel._calendar.pop(key, None)
        else:
            hotel._calendar[key] = new_value

        current += timedelta(days=1)


def make_reservation(hotels: list, customers: list) -> None:
    print("\nType 'cancel' at any time to return to the main menu.\n")

    hotel_id = prompt_int("Hotel ID: ")
    customer_id = prompt_int("Customer ID: ")

    hotel = find_hotel(hotels, hotel_id)
    if hotel is None:
        raise ValueError("Hotel not found.")

    customer = find_customer(customers, customer_id)
    if customer is None:
        raise ValueError("Customer not found.")

    start_date = prompt_input("Start date YYYY-MM-DD (type 'cancel' to return): ")
    end_date = prompt_input("End date YYYY-MM-DD (type 'cancel' to return): ")
    rooms = prompt_int("Rooms to reserve (type 'cancel' to return): ")

    if not hotel.available_rooms_for_dates(start_date, end_date, rooms):
        raise ValueError("No rooms available for the selected dates.")

    apply_calendar_change(hotel, start_date, end_date, rooms, sign=1)
    print("Reservation applied to hotel calendar.")


def save_all(hotels: list, customers: list) -> None:
    save_hotels_to_file(hotels, HOTELS_FILE)
    save_customers_to_file(customers, CUSTOMERS_FILE)
    print("Data saved.")


def main():
    hotels = load_hotels_from_file(HOTELS_FILE)
    customers = load_customers_from_file(CUSTOMERS_FILE)

    while True:
        print("\nMain Menu")
        print("1. Create Hotel")
        print("2. List Hotels")
        print("3. Consult Hotel")
        print("4. Delete Hotel")
        print("5. Create Customer")
        print("6. List Customers")
        print("7. Consult Customer")
        print("8. Delete Customer")
        print("9. Make Reservation")
        print("10. Save and Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                create_hotel(hotels)
                pause()
            elif choice == "2":
                list_hotels(hotels)
                pause()
            elif choice == "3":
                consult_hotel(hotels)
                pause()
            elif choice == "4":
                delete_hotel(hotels)
                pause()
            elif choice == "5":
                create_customer(customers)
                pause()
            elif choice == "6":
                list_customers(customers)
                pause()
            elif choice == "7":
                consult_customer(customers)
                pause()
            elif choice == "8":
                delete_customer(customers)
                pause()
            elif choice == "9":
                make_reservation(hotels, customers)
                pause()
            elif choice == "10":
                save_all(hotels, customers)
                print("Bye.")
                break
            else:
                print("Invalid option.")
                pause()
        except CancelOperation:
            print("Operation cancelled.")
            pause()
        except (ValueError, TypeError) as exc:
            print(f"Error: {exc}")
            pause()

if __name__ == "__main__":
    main()