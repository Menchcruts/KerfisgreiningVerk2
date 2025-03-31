import factory, faker
import factory.random
from datetime import datetime, timedelta, date

# faker.Faker().date_time_between
# faker.Faker().date_time()

from src.models.Booking import Booking
from .AppCategoryFactory import AppCategoryFactory

class BookingFactory(factory.Factory[Booking]):
    class Meta:
        model = Booking

    Start = factory.Faker("date_time_between", start_date=date.today() - timedelta(days=10), end_date=date.today() + timedelta(days=10))
    # End = factory.LazyAttribute(lambda obj: obj.Start + timedelta(hours=factory.random.randgen.randint(1,3)))
    End = factory.LazyAttribute(lambda obj: faker.Faker().date_time_between(start_date=obj.Start, end_date=obj.Start + timedelta(hours=8)))

    Category = factory.SubFactory(AppCategoryFactory)