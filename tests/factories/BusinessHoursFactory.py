import factory, faker
import factory.random
from datetime import time

faker.Faker().time_object()

from src.models.BusinessHours import BusinessHours

class BusinessHoursFactory(factory.Factory[BusinessHours]):
    class Meta:
        model = BusinessHours

    dayOfWeek = factory.Faker("day_of_week")
    openTime = factory.Faker("time_object")
    closeTime = factory.Faker("time_object")

    # openTime = time(hour=factory.random.randgen.randint(7, 9))
    # closeTime = factory.LazyAttribute(lambda obj: time(hour=obj.openTime.hour + factory.Faker("random_int", min=4, max=8)))