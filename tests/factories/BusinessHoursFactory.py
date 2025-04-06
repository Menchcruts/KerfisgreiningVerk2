import factory, faker
from datetime import datetime, time, date

from ...src.models.BusinessHours import BusinessHours

faker.Faker().time_object()

class BusinessHoursFactory(factory.Factory[BusinessHours]):
    """
    It's best to create an instance with .create() instead of the constructor.
    """
    class Meta:
        model = BusinessHours

    dayOfWeek = factory.Faker("day_of_week")
    openTime = factory.Faker("time_object")
    closeTime = factory.LazyAttribute(lambda obj: faker.Faker().date_time_between(start_date=datetime.combine(date.today(), obj.openTime), end_date=datetime.combine(date.today(), time.max)).time())

    # openTime = time(hour=factory.random.randgen.randint(7, 9))
    # closeTime = factory.LazyAttribute(lambda obj: time(hour=obj.openTime.hour + factory.Faker("random_int", min=4, max=8)))