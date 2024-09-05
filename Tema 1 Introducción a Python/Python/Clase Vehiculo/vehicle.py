#!/usr/bin/python3

class Vehicle:
    person_price = 10  # € /person

    def __init__(self, capacity):
        self.capacity = capacity

    def fare(self):
        return self.capacity * self.person_price


if __name__ == '__main__':  # SI EJECUTO EL SCRIPT PRINCIPAL, NO LO IMPORTO
    ve = Vehicle(6)
    print("Vehicle capacity:", ve.capacity, "Vehicle fare: ", ve.fare())
