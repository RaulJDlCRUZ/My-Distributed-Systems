#!/usr/bin/python3

from vehicle import Vehicle


class Car(Vehicle):
    person_price = 20  # € / persona, diferente a coche

    def __init__(self, capacity):
        super().__init__(capacity)

if __name__ == '__main__':
    car = Car(6)
    print("Vehicle capacity:", car.capacity, "Vehicle fare: ", car.fare())
