from src.models.BusinessHours import BusinessHours
from src.models.User import User
from src.models.AppointmentCategory import AppointmentCategory
from datetime import time

test = BusinessHours("Monday", time(hour=8), time(hour=16))
print(test)
print(repr(test))
print()

user1 = User("Jóel", "joelarnar@gmail.com")
print(repr(user1))
print()

test2 = AppointmentCategory("Yoga", 120, 2)
print(test2)
print(repr(test2))