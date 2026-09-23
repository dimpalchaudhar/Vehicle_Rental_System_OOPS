import streamlit as st
from abc import ABC, abstractmethod

# Abstract Base Class
class Vehicle(ABC):
    def __init__(self, vehicle_id, brand, model, rental_price):
        self.vehicle_id = vehicle_id
        self.brand = brand
        self.model = model
        self.rental_price = rental_price
        self.available = True

    @abstractmethod
    def calculate_rental_cost(self, days):
        pass

# Derived Classes
class Car(Vehicle):
    def __init__(self, vehicle_id, brand, model, rental_price, seats):
        super().__init__(vehicle_id, brand, model, rental_price)
        self.seats = seats

    def calculate_rental_cost(self, days):
        return self.rental_price * days

class Bike(Vehicle):
    def __init__(self, vehicle_id, brand, model, rental_price, engine_cc):
        super().__init__(vehicle_id, brand, model, rental_price)
        self.engine_cc = engine_cc

    def calculate_rental_cost(self, days):
        return (self.rental_price * days) - 50  ## discount for bikes

class Truck(Vehicle):
    def __init__(self, vehicle_id, brand, model, rental_price, load_capacity):
        super().__init__(vehicle_id, brand, model, rental_price)
        self.load_capacity = load_capacity

    def calculate_rental_cost(self, days):
        return (self.rental_price * days) + 200 ## extra chnarge for trucks


## Customer class
class Customer:
    def __init__(self, customer_id, name, contact):
        self.customer_id = customer_id
        self.name = name
        self.contact = contact


# Rental Class
class Rental:
    def __init__(self, customer, vehicle, days):
        self.customer = customer
        self.vehicle = vehicle
        self.days = days
        self.cost = vehicle.calculate_rental_cost(days)
        vehicle.available = False

    def return_vehicle(self):
        self.vehicle.available = True
        print(f"{self.customer.name} returned {self.vehicle.model}")


# Rental System
class RentalSystem:
    def __init__(self):
        self.vehicles = []
        self.customers = []
        self.rentals = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def add_customer(self, customer):
        self.customers.append(customer)

    def rent_vehicle(self, customer_id, vehicle_id, days):
        customer = next((c for c in self.customers if c.customer_id == customer_id), None)
        vehicle = next((v for v in self.vehicles if v.vehicle_id == vehicle_id and v.available), None)
        if customer and vehicle:
            rental = Rental(customer, vehicle, days)
            self.rentals.append(rental)
            print(f"{customer.name} rented {vehicle.model} for {days} days. Cost: {rental.cost}")
        else:
            print("Vehicle not available or customer not found.")


## Streamlit UI
st.title("Vehicle Rental System")

## Demo
system = RentalSystem()
system.add_vehicle(Car(1, "Toyota", "Corolla", 1000, 5))
system.add_vehicle(Bike(2, "Honda", "CBR", 500, 150))
system.add_vehicle(Truck(3, "Tata", "HeavyDuty", 2000, 1000))

system.add_customer(Customer(101, "Dimpal", "80105769750"))


## UI Inputs
st.header("Book a Vehicle")
days = st.number_input("Enter rental days", min_value=1, step=1)
vehicle_choice = st.selectbox("Choose a vehicle", [f"{v.vehicle_id} - {v.model}" for v in system.vehicles if v.available])

if st.button("Rent Vehicle"):
    if vehicle_choice:
        vehicle_id = int(vehicle_choice.split(" - ")[0])
        system.rent_vehicle(101, vehicle_id, days)
        st.success(f"Vehicle rented successfully for {days} days.")
    else:
        st.error("No available vehicles to rent.")


# Show rentals
st.header("Current Rentals")
for rental in system.rentals:
    st.write(f"{rental.customer.name} -> {rental.vehicle.model} ({rental.days} days) | Cost: {rental.cost}")
