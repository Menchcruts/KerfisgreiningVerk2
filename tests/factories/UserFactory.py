import factory

from src.models.User import User

class UserFactory(factory.Factory[User]):
    class Meta:
        model = User

    name = factory.Faker("name")
    email = factory.Faker("email")