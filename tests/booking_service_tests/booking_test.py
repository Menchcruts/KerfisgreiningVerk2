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

def test_booking_outside_business_hours():
    bs = BookingService()
    user = UserFactory.create()
    business = Business("Late Booking Business")

    hours = BusinessHoursFactory.create(dayOfWeek="Monday", openTime=time(9, 0), closeTime=time(17, 0))
    business.addBusinessHours(hours)

    ac = AppCategoryFactory.create(lengthInMinutes=60)
    business.addAppointmentCategory(ac)

    
    booking_time = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)

    result = bs.isAvailableForBooking(business, ac, booking_time)

    assert not result, "Should not allow booking outside business hours"


def test_overlapping_booking():
    bs = BookingService()
    user = UserFactory.create()
    business = Business("Overlap Biz")

    hours = BusinessHoursFactory.create(dayOfWeek="Monday", openTime=time(9, 0), closeTime=time(17, 0))
    business.addBusinessHours(hours)

    ac = AppCategoryFactory.create(lengthInMinutes=120)
    business.addAppointmentCategory(ac)

   
    start_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(minutes=120)
    existing_booking = BookingFactory.create(user=user, Start=start_time, End=end_time, Category=ac)
    business.bookings.append(existing_booking)

    
    overlap_time = start_time + timedelta(hours=1)

    result = bs.isAvailableForBooking(business, ac, overlap_time)

    assert not result, "Should not allow overlapping bookings"


def test_non_overlapping_booking():
    bs = BookingService()
    user = UserFactory.create()
    business = Business("Gap Biz")

    hours = BusinessHoursFactory.create(dayOfWeek="Monday", openTime=time(9, 0), closeTime=time(17, 0))
    business.addBusinessHours(hours)

    ac = AppCategoryFactory.create(lengthInMinutes=120)
    business.addAppointmentCategory(ac)


    start_time = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(minutes=120)
    existing_booking = BookingFactory.create(user=user, Start=start_time, End=end_time, Category=ac)
    business.bookings.append(existing_booking)

    
    non_overlap_time = end_time + timedelta(minutes=1)

    result = bs.isAvailableForBooking(business, ac, non_overlap_time)

    assert result, "Should allow non-overlapping bookings"