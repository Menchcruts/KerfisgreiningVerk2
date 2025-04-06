from dataclasses import dataclass

from ..models.Business import Business
from ..models.User import User
from ..models.BusinessHours import BusinessHours
from ..models.Booking import Booking
from ..models.AppointmentCategory import AppointmentCategory

from datetime import datetime, timedelta


class BookingService:
    
    def __init__(self):
        self.bookings:dict[str, Booking] = {}

    @staticmethod
    def isAvailableForBooking(
            business: Business, 
            appointmentCategory: AppointmentCategory,
            scheduledTime: datetime
            ) -> bool:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        day_of_week = days[scheduledTime.weekday()]
        business_hours = None
        for hour in business.businessHours:
            if hour.dayOfWeek == day_of_week:
                business_hours = hour
                break

        # business_hours = business.businessHours.get(day_of_week, None)

        if not business_hours:
            print(f"Business is closed on {day_of_week}.")
            return False

        opening_time = datetime.combine(scheduledTime.date(), business_hours.openTime)
        closing_time = datetime.combine(scheduledTime.date(), business_hours.closeTime)

        appointment_end_time = scheduledTime + timedelta(minutes=appointmentCategory.lengthInMinutes)

        if scheduledTime < opening_time or appointment_end_time > closing_time:
            print(f"Appointment time {scheduledTime} is outside business hours ({opening_time} - {closing_time}).")
            return False

        return True


    def createBooking(
            self,
            user:User, 
            appointmentCategory:AppointmentCategory, 
            scheduledTime:datetime
            ) -> Booking:

        endTime = scheduledTime + timedelta(minutes=appointmentCategory.lengthInMinutes)

        booking = Booking(
            user=user,
            Start=scheduledTime, 
            End=endTime, 
            Category=appointmentCategory)

        self.bookings[str(booking.id)] = booking

        return booking
    
    def cancelBooking(self, booking:Booking, user: User) -> bool:
        if booking.user == user and booking.canBeCancelled():
            if str(booking.id) in self.bookings:
                del self.bookings[str(booking.id)]
                return True
        return False

    def getBookingsForUser(self, user_id) -> list[Booking]:
        user_bookings = [booking for booking in self.bookings.values() if booking.user == user_id]
        return user_bookings
    
    