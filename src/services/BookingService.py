from ..models.Business import Business
from ..models.User import User
from ..models.BusinessHours import BusinessHours
from ..models.Booking import Booking
from ..models.AppointmentCategory import AppointmentCategory

from datetime import datetime, timedelta


class BookingService:
    
    @staticmethod
    def isAvailableForBooking(
            business: Business, 
            appointmentCategory:AppointmentCategory,
            scheduledTime: datetime
            ) -> bool:
        ...

    @staticmethod
    def createBooking(
            user:User, 
            appointmentCategory:AppointmentCategory, 
            scheduledTime:datetime
            ) -> Booking:
        ...
    
    @staticmethod
    def cancelBooking(booking:Booking, user: User) -> bool:
        ...

    @staticmethod
    def getBookingsForUser(user: User) -> list[Booking]:
        ...