from ..models.Business import Business
from ..models.User import User
from ..models.BusinessHours import BusinessHours
from ..models.Booking import Booking
from ..models.AppointmentCategory import AppointmentCategory

from datetime import datetime, timedelta


class BookingService:
    
    def isAvailableForBooking(
            business: Business, 
            appointmentCategory:AppointmentCategory,
            scheduledTime: datetime
            ) -> bool:
        ...

    def createBooking(
            user:User, 
            appointmentCategory:AppointmentCategory, 
            scheduledTime:datetime
            ) -> Booking:
        ...
    
    def cancelBooking(booking:Booking, user: User) -> bool:
        ...

    def getBookingsForUser(user: User) -> list[Booking]:
        ...