"""
CLI menu for the A6.2 Reservation System.

Provides a console interface to manage hotels, customers, and reservations.
"""

# pylint: disable=duplicate-code


from typing import List, Optional

from source.customer import (
    Customer,
    load_customers_from_file,
    save_customers_to_file,
)
from source.hotel import (
    Hotel,
    load_hotels_from_file,
    save_hotels_to_file,
)
from source.reservation import (
    Reservation,
    load_reservations_from_file,
    save_reservations_to_file,
)

HOTELS_FILE = "hotels.json"
CUSTOMERS_FILE = "customers.json"
RESERVATIONS_FILE = "reservations.json"


class CancelOperation(Exception):
    """Raised when the user cancels the current operation."""


def prompt_input(message: str) -> str:
    """Prompt a string input. Typing 'cancel' raises CancelOperation."""
    value = input(message).strip()
    if value.lower() == "cancel":
        raise CancelOperation()
    return value


def prompt_int(message: str) -> int:
    """Prompt an integer input. Typing 'cancel' raises CancelOperation."""
    value = prompt_input(message)
    return int(value)


def pause() -> None:
    """Pause the program until the user presses Enter."""
    input("\nPress Enter to continue...")


def show_cancel_legend() -> None:
    """Show the cancel instruction for the current menu."""
    print("\nType 'cancel' at any time to return to the previous menu.\n")


def find_hotel(hotels: List[Hotel], hotel_id: int) -> Optional[Hotel]:
    """Find a hotel by ID in a list of hotels."""
    for hotel in hotels:
        if hotel.hotel_id == hotel_id:
            return hotel
    return None


def find_customer(
        customers: List[Customer],
        customer_id: int
        ) -> Optional[Customer]:
    """Find a customer by ID in a list of customers."""
    for customer in customers:
        if customer.customer_id == customer_id:
            return customer
    return None


def find_reservation(
    reservations: List[Reservation], reservation_id: int
) -> Optional[Reservation]:
    """Find a reservation by ID in a list of reservations."""
    for reservation in reservations:
        if reservation.reservation_id == reservation_id:
            return reservation
    return None


def create_hotel(hotels: List[Hotel]) -> None:
    """Create a new hotel and add it to the hotels list."""
    show_cancel_legend()
    hotel_id = prompt_int("Hotel ID: ")
    name = prompt_input("Name: ")
    location = prompt_input("Location: ")
    total_rooms = prompt_int("Total rooms: ")

    if find_hotel(hotels, hotel_id) is not None:
        raise ValueError("Hotel ID already exists.")

    hotels.append(Hotel(hotel_id, name, location, total_rooms))
    print("Hotel created.")


def list_hotels(hotels: List[Hotel]) -> None:
    """Print all hotels with basic information."""
    if not hotels:
        print("No hotels found.")
        return

    for hotel in hotels:
        print(
            {
                "hotel_id": hotel.hotel_id,
                "name": hotel.name,
                "location": hotel.location,
                "total_rooms": hotel.total_rooms,
            }
        )


def display_hotel_information(hotels: List[Hotel]) -> None:
    """Display a single hotel information by ID."""
    show_cancel_legend()
    hotel_id = prompt_int("Hotel ID: ")
    hotel = find_hotel(hotels, hotel_id)
    if hotel is None:
        raise ValueError("Hotel not found.")

    print(
        {
            "hotel_id": hotel.hotel_id,
            "name": hotel.name,
            "location": hotel.location,
            "total_rooms": hotel.total_rooms,
        }
    )


def modify_hotel(hotels: List[Hotel]) -> None:
    """Modify hotel information."""
    show_cancel_legend()
    hotel_id = prompt_int("Hotel ID: ")
    hotel = find_hotel(hotels, hotel_id)
    if hotel is None:
        raise ValueError("Hotel not found.")

    print("Leave empty to keep current value.")
    name = input("New name: ").strip()
    location = input("New location: ").strip()

    if name == "":
        name = None
    if location == "":
        location = None

    hotel.modify_information(name=name, location=location)
    print("Hotel updated.")


def delete_hotel(hotels: List[Hotel], reservations: List[Reservation]) -> None:
    """Delete a hotel if it has no existing reservations."""
    show_cancel_legend()
    hotel_id = prompt_int("Hotel ID to delete: ")

    for reservation in reservations:
        if reservation.hotel_id == hotel_id:
            raise ValueError("Cannot delete hotel with existing reservations.")

    for idx, hotel in enumerate(hotels):
        if hotel.hotel_id == hotel_id:
            hotels.pop(idx)
            print("Hotel deleted.")
            return

    raise ValueError("Hotel not found.")


def create_customer(customers: List[Customer]) -> None:
    """Create a new customer and add it to the customers list."""
    show_cancel_legend()
    customer_id = prompt_int("Customer ID: ")
    name = prompt_input("Name: ")
    email = prompt_input("Email: ")

    if find_customer(customers, customer_id) is not None:
        raise ValueError("Customer ID already exists.")

    customers.append(Customer(customer_id, name, email))
    print("Customer created.")


def list_customers(customers: List[Customer]) -> None:
    """Print all customers."""
    if not customers:
        print("No customers found.")
        return

    for customer in customers:
        print(customer.to_dict())


def display_customer_information(customers: List[Customer]) -> None:
    """Display a single customer information by ID."""
    show_cancel_legend()
    customer_id = prompt_int("Customer ID: ")
    customer = find_customer(customers, customer_id)
    if customer is None:
        raise ValueError("Customer not found.")
    print(customer.to_dict())


def modify_customer(customers: List[Customer]) -> None:
    """Modify customer information."""
    show_cancel_legend()
    customer_id = prompt_int("Customer ID: ")
    customer = find_customer(customers, customer_id)
    if customer is None:
        raise ValueError("Customer not found.")

    print("Leave empty to keep current value.")
    name = input("New name: ").strip()
    email = input("New email: ").strip()

    if name != "":
        customer.name = name
    if email != "":
        customer.email = email

    if not customer.name:
        raise ValueError("Customer name cannot be empty.")
    if not customer.email:
        raise ValueError("Customer email cannot be empty.")

    print("Customer updated.")


def delete_customer(
        customers: List[Customer],
        reservations: List[Reservation]
        ) -> None:
    """Delete a customer if it has no existing reservations."""
    show_cancel_legend()
    customer_id = prompt_int("Customer ID to delete: ")

    for reservation in reservations:
        if reservation.customer_id == customer_id:
            raise ValueError(
                "Cannot delete customer with existing reservations."
                )

    for idx, customer in enumerate(customers):
        if customer.customer_id == customer_id:
            customers.pop(idx)
            print("Customer deleted.")
            return

    raise ValueError("Customer not found.")


def create_reservation(
    hotels: List[Hotel],
    customers: List[Customer],
    reservations: List[Reservation],
) -> None:
    """Create a reservation and apply it to the hotel calendar."""
    show_cancel_legend()
    reservation_id = prompt_int("Reservation ID: ")
    if find_reservation(reservations, reservation_id) is not None:
        raise ValueError("Reservation ID already exists.")

    hotel_id = prompt_int("Hotel ID: ")
    customer_id = prompt_int("Customer ID: ")

    hotel = find_hotel(hotels, hotel_id)
    if hotel is None:
        raise ValueError("Hotel not found.")

    customer = find_customer(customers, customer_id)
    if customer is None:
        raise ValueError("Customer not found.")

    start_date = prompt_input("Start date YYYY-MM-DD: ")
    end_date = prompt_input("End date YYYY-MM-DD: ")
    rooms = prompt_int("Rooms to reserve: ")

    if not hotel.available_rooms_for_dates(start_date, end_date, rooms):
        raise ValueError("No rooms available for the selected dates.")

    hotel.apply_calendar_change(start_date, end_date, rooms, sign=1)

    reservations.append(
        Reservation(
            reservation_id=reservation_id,
            hotel_id=hotel_id,
            customer_id=customer_id,
            start_date=start_date,
            end_date=end_date,
            rooms_reserved=rooms,
        )
    )

    print("Reservation created.")


def cancel_reservation(
        hotels: List[Hotel],
        reservations: List[Reservation]
        ) -> None:
    """Cancel a reservation and revert the hotel calendar."""
    show_cancel_legend()
    reservation_id = prompt_int("Reservation ID to cancel: ")
    reservation = find_reservation(reservations, reservation_id)
    if reservation is None:
        raise ValueError("Reservation not found.")

    hotel = find_hotel(hotels, reservation.hotel_id)
    if hotel is None:
        raise ValueError("Hotel not found.")

    hotel.apply_calendar_change(
        reservation.start_date,
        reservation.end_date,
        reservation.rooms_reserved,
        sign=-1,
    )

    reservations.remove(reservation)
    print("Reservation cancelled.")


def list_reservations(reservations: List[Reservation]) -> None:
    """Print all reservations."""
    if not reservations:
        print("No reservations found.")
        return

    for reservation in reservations:
        print(reservation.to_dict())


def save_all(
    hotels: List[Hotel],
    customers: List[Customer],
    reservations: List[Reservation],
) -> None:
    """Save hotels, customers, and reservations to their JSON files."""
    save_hotels_to_file(hotels, HOTELS_FILE)
    save_customers_to_file(customers, CUSTOMERS_FILE)
    save_reservations_to_file(reservations, RESERVATIONS_FILE)
    print("Data saved.")


def hotels_menu(
        hotels: List[Hotel],
        reservations: List[Reservation]
        ) -> None:
    """Show the hotels submenu."""
    while True:
        print("\nHotels Menu")
        print("1. Create Hotel")
        print("2. List Hotels")
        print("3. Display Hotel information")
        print("4. Modify Hotel Information")
        print("5. Delete Hotel")
        print("6. Back")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                create_hotel(hotels)
                pause()
            elif choice == "2":
                list_hotels(hotels)
                pause()
            elif choice == "3":
                display_hotel_information(hotels)
                pause()
            elif choice == "4":
                modify_hotel(hotels)
                pause()
            elif choice == "5":
                delete_hotel(hotels, reservations)
                pause()
            elif choice == "6":
                return
            else:
                print("Invalid option.")
                pause()
        except CancelOperation:
            print("Operation cancelled.")
            pause()
        except (ValueError, TypeError) as exc:
            print(f"Error: {exc}")
            pause()


def customers_menu(
        customers: List[Customer],
        reservations: List[Reservation]
        ) -> None:
    """Show the customers submenu."""
    while True:
        print("\nCustomers Menu")
        print("1. Create Customer")
        print("2. List Customers")
        print("3. Display Customer Information")
        print("4. Modify Customer Information")
        print("5. Delete Customer")
        print("6. Back")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                create_customer(customers)
                pause()
            elif choice == "2":
                list_customers(customers)
                pause()
            elif choice == "3":
                display_customer_information(customers)
                pause()
            elif choice == "4":
                modify_customer(customers)
                pause()
            elif choice == "5":
                delete_customer(customers, reservations)
                pause()
            elif choice == "6":
                return
            else:
                print("Invalid option.")
                pause()
        except CancelOperation:
            print("Operation cancelled.")
            pause()
        except (ValueError, TypeError) as exc:
            print(f"Error: {exc}")
            pause()


def reservations_menu(
    hotels: List[Hotel],
    customers: List[Customer],
    reservations: List[Reservation],
) -> None:
    """Show the reservations submenu."""
    while True:
        print("\nReservations Menu")
        print("1. Create a Reservation")
        print("2. Cancel a Reservation")
        print("3. List Reservations")
        print("4. Back")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                create_reservation(hotels, customers, reservations)
                pause()
            elif choice == "2":
                cancel_reservation(hotels, reservations)
                pause()
            elif choice == "3":
                list_reservations(reservations)
                pause()
            elif choice == "4":
                return
            else:
                print("Invalid option.")
                pause()
        except CancelOperation:
            print("Operation cancelled.")
            pause()
        except (ValueError, TypeError) as exc:
            print(f"Error: {exc}")
            pause()


def main() -> None:
    """Program entry point."""
    hotels = load_hotels_from_file(HOTELS_FILE)
    customers = load_customers_from_file(CUSTOMERS_FILE)
    reservations = load_reservations_from_file(RESERVATIONS_FILE)

    while True:
        print("\nMain Menu")
        print("1. Hotels")
        print("2. Customers")
        print("3. Reservations")
        print("4. Save and Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            hotels_menu(hotels, reservations)
        elif choice == "2":
            customers_menu(customers, reservations)
        elif choice == "3":
            reservations_menu(hotels, customers, reservations)
        elif choice == "4":
            save_all(hotels, customers, reservations)
            print("Bye.")
            break
        else:
            print("Invalid option.")
            pause()


if __name__ == "__main__":
    main()
