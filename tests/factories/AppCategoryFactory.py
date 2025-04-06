import factory, random
import factory.random

from ...src.models.AppointmentCategory import AppointmentCategory

class AppCategoryFactory(factory.Factory[AppointmentCategory]):
    """
    It's best to create an instance with .create() instead of the constructor.
    """
    class Meta:
        model = AppointmentCategory

    name = factory.Faker("name")

    # Jóel: 
    # Galli við random er að öll object búin til með verksmiðjunni hafa sömu random gildin
    # Veit ekki alveg hvernig ég laga það.
    
    # lengthInMinutes = factory.random.randgen.randint(1, 5) * 60

    # Þetta er quick fix. Ætti að vera allt í lagi.
    lengthInMinutes = factory.Faker("random_int", min=60, max=300)

    minNumOfHoursBeforeCancellation = factory.Faker("random_int", min=1, max=5)