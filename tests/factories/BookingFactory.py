import factory, faker
from datetime import datetime, timedelta, date, time

from src.models.Booking import Booking
from .AppCategoryFactory import AppCategoryFactory

class BookingFactory(factory.Factory[Booking]):
    """
    It's best to create an instance with .create() instead of the constructor.
    """
    class Meta:
        model = Booking

    Start = factory.Faker("date_time_between", start_date=date.today() - timedelta(days=10), end_date=date.today() + timedelta(days=10))
    End = factory.LazyAttribute(lambda obj: faker.Faker().date_time_between(start_date=obj.Start, end_date=datetime.combine(obj.Start.date(), time.max)))

    Category = factory.SubFactory(AppCategoryFactory)