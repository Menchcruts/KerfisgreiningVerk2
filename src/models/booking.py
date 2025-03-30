from datetime import datetime, timedelta
from user import User
from appointmentCategory import AppointmentCategory

class Booking:
    def __init__(self, booking_id: int, user: User, appointment_category: AppointmentCategory, scheduled_start: datetime):
        self.booking_id = booking_id
        self.user = user
        self.appointment_category = appointment_category
        self.scheduled_start = scheduled_start
        self.scheduled_end = self.scheduled_start + timedelta(minutes=appointment_category.length_in_minutes)
        self.cancellation_deadline = self.calculate_cancellation_deadline()

    def calculate_cancellation_deadline(self):
        """Returns the latest time a booking can be canceled."""
        return self.scheduled_start - timedelta(hours=self.appointment_category.min_hours_before_cancellation)

    def can_be_cancelled(self):
        """Checks if the booking can still be canceled."""
        return datetime.now() <= self.cancellation_deadline

    def __repr__(self):
        return f"Booking(id={self.booking_id}, user={self.user.name}, service={self.appointment_category.name}, date={self.scheduled_start}, cancel_by={self.cancellation_deadline})"
