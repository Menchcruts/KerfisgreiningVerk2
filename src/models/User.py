from dataclasses import dataclass, field
import uuid

@dataclass
class User:
    id: uuid.UUID = field(init=False, default_factory=uuid.uuid1)
    name: str
    email: str
    
    users = []
    
    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name:
            raise ValueError(f"{self.name} is not a non empty str")
        if not isinstance(self.email, str) or not self.email:
            raise ValueError(f"{self.email} is not a non empty str")
        if "@" not in self.email:
            raise ValueError(f"{self.email} is not a valid email address")
        
    @classmethod
    def get_user_by_id(self, user_id: str):
        for user in User.users:
            if str(user.id) == user_id:
                return user
        return None


    def __str__(self):
        return f"{self.name} - {self.email}"