from dataclasses import dataclass, field
import uuid

@dataclass
class User:
    id: uuid.UUID = field(init=False, default_factory=uuid.uuid1)
    name: str
    email: str

    def __str__(self):
        return f"{self.name} - {self.email}"