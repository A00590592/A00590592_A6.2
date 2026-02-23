# Hotel Management System – A6.2

Repository for Activity 6.2 – Software Development with Static Analysis and Testing.

This project implements a simple hotel reservation system in Python following PEP 8 standards and validated using pylint and unit testing.

## Project Structure

The project is organized using the following directory structure:

A6.2/

├─ source/

├─ tests/

├─ results/

└─ pylint/

## Folder Description

source/
Contains the Python source code for the hotel management system.

Includes:

customer.py | hotel.py | reservation.py | menu.py

The main program (menu.py) must be executed from this directory using the command line.

tests/
Contains the unit test files used to validate program behavior.

Includes:

test_customer.py | test_hotel.py | test_reservation.py

All test cases are executed using the unittest framework.

results/
Stores output files generated during execution, including:

Coverage reports
Generated JSON persistence files (hotels, customers, reservations)

pylint/
Contains the static analysis reports generated using:

pylint | flake8

## Program Description

The system allows:

Creation, modification, and deletion of hotels

Creation, modification, and deletion of customers

Reservation and cancellation of rooms

Date range validation and availability checking

JSON file persistence for system data

The program includes proper exception handling and input validation.

All modules comply with PEP 8 coding standards.

