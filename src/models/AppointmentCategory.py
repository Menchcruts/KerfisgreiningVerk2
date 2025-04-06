from dataclasses import dataclass, field
import uuid


@dataclass
class AppointmentCategory:
    id: uuid.UUID = field(init=False, default_factory=uuid.uuid1)
    name: str
    lengthInMinutes: int
    minNumOfHoursBeforeCancellation: int

    def __str__(self):
        return f"{self.name} - {self.lengthInMinutes} minutes | Cancellation deadline: {self.minNumOfHoursBeforeCancellation} hours before"