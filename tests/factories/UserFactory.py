import factory

from src.models.User import User

class UserFactory(factory.Factory[User]):
    """
    It's best to create an instance with .create() instead of the constructor.
    """
    class Meta:
        model = User

    name = factory.Faker("name")
    email = factory.Faker("email")