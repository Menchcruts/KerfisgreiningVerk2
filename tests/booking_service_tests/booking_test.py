# bambambini goozini
import factory
import pytest
from datetime import datetime, timedelta, time

from ...src.services.BookingService import BookingService
from ...src.models.Business import Business

from ..factories.AppCategoryFactory import AppCategoryFactory
from ..factories.BookingFactory import BookingFactory
from ..factories.UserFactory import UserFactory
from ..factories.BusinessHoursFactory import BusinessHoursFactory

def test_valid_booking():
    business = Business("test")
    
    start = time(hour=8)
    end = time(hour=16)
    hours = BusinessHoursFactory.create(dayOfWeek="Sunday", openTime=start, closeTime=end)
    assert hours.dayOfWeek == "Sunday"

    business.addBusinessHours(hours)

    ac = AppCategoryFactory.create(lengthInMinutes=120)
    business.addAppointmentCategory(ac)

    test_time = datetime.now().replace(hour=9)

    bs = BookingService()
    result = bs.isAvailableForBooking(business, ac, test_time)

    assert result, "Should allow available booking"

@pytest.mark.skip("bara")
def test_booking_within_business_hours():

    business_hours = BusinessHoursFactory.create(open_time=datetime.now().replace(hour=9, minute=0, second=0, microsecond=0),
                                                  close_time=datetime.now().replace(hour=17, minute=0, second=0, microsecond=0))

    booking_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    booking = BookingFactory.create(scheduledTime=booking_time, business=business_hours.business)

    bs = BookingService()
    result = bs.isAvailableForBooking(booking.business, booking.appointmentCategory, booking.scheduledTime)

    assert result, "Should allow booking within business hours"

def test_booking_outside_business_hours():

    business_hours = BusinessHoursFactory.create(open_time=datetime.now().replace(hour=9, minute=0, second=0, microsecond=0),
                                                  close_time=datetime.now().replace(hour=17, minute=0, second=0, microsecond=0))

    booking_time = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
    booking = BookingFactory.create(scheduledTime=booking_time, business=business_hours.business)

    bs = BookingService()
    result = bs.isAvailableForBooking(booking.business, booking.appointmentCategory, booking.scheduledTime)

    assert not result, "Should not allow booking outside business hours"

def test_overlapping_booking():

    start_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=2)


    existing_booking = BookingFactory.create(start_time=start_time, end_time=end_time)


    overlapping_start_time = start_time + timedelta(hours=1)
    new_booking = BookingFactory.create(start_time=overlapping_start_time)

    bs = BookingService()
    result = bs.isAvailableForBooking(new_booking.business, new_booking.appointmentCategory, new_booking.scheduledTime)

    assert not result, "Should not allow overlapping bookings"

def test_non_overlapping_booking():

    start_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(hours=2)


    existing_booking = BookingFactory.create(start_time=start_time, end_time=end_time)

    non_overlapping_start_time = end_time + timedelta(minutes=1)  # Starts 1 minute after the previous booking ends
    new_booking = BookingFactory.create(start_time=non_overlapping_start_time)

    bs = BookingService()
    result = bs.isAvailableForBooking(new_booking.business, new_booking.appointmentCategory, new_booking.scheduledTime)

    assert result, "Should allow non-overlapping bookings"