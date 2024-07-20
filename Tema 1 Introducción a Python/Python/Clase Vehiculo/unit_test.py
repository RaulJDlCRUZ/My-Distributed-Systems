#!/usr/bin/python3
from unittest import TestCase
from vehicle import Vehicle
from car import Car


class TestVehicle(TestCase):
    def setUp(self):
        self.vehicle = Vehicle(6)  # Guardamos como atributo
        pass  # en blanco, pasa a lo siguiente

    def test_default_fare_60(self):
        self.assertEqual(self.vehicle.fare(), 60)
        pass


class TestCar(TestCase):
    def setUp(self):
        self.car = Car(6)

    def test_default_fare_120(self):
        self.assertEqual(self.car.fare(), 120)
