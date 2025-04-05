from ..models.Business import Business
from ..models.User import User
from ..models.BusinessHours import BusinessHours
from ..models.Booking import Booking
from ..models.AppointmentCategory import AppointmentCategory

from datetime import datetime, timedelta


class BookingService:
    
    def __init__(self):
        self.bookings = []  

    @staticmethod
    def isAvailableForBooking(
            business: Business, 
            appointmentCategory:AppointmentCategory,
            scheduledTime: datetime
            ) -> bool:
        
        day_of_week = scheduledTime.strftime("%A")
        business_hours = business.getBusinessHoursForDay(day_of_week)

        if not business_hours:
            return False

        # Build full datetime ranges for comparison
        opening_time = datetime.combine(scheduledTime.date(), business_hours.openingTime)
        closing_time = datetime.combine(scheduledTime.date(), business_hours.closingTime)

        appointment_end_time = scheduledTime + timedelta(minutes=appointmentCategory.lengthInMinutes)

        if scheduledTime < opening_time or appointment_end_time > closing_time:
            return False

        # Check for overlaps with existing bookings
        for booking in business.getBookings():
            if scheduledTime < booking.scheduledEndTime and appointment_end_time > booking.scheduledStartTime:
                return False


    @staticmethod
    def createBooking(
            self,
            user:User, 
            appointmentCategory:AppointmentCategory, 
            scheduledTime:datetime
            ) -> Booking:
        
        endTime = scheduledTime + timedelta(minutes=appointmentCategory.lengthInMinutes)

        booking = Booking(
            Start=scheduledTime, 
            End=endTime, 
            Category=appointmentCategory)

        self.bookings.append(booking)

        return booking
    
    @staticmethod
    def cancelBooking(self, booking:Booking, user: User) -> bool:
        if booking.user == user and booking.canBeCancelled():
            if booking in self.bookings:
                self.bookings.remove(booking)
                return True
        return False  

    @staticmethod
    def getBookingsForUser(self, user: User) -> list[Booking]:
        return [booking for booking in self.bookings if hasattr(booking, 'user') and booking.user == user]