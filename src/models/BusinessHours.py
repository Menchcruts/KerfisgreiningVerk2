from dataclasses import dataclass, field
import datetime
import uuid

@dataclass
class BusinessHours:
    id: uuid.UUID = field(default_factory=uuid.uuid1, init=False)
    dayOfWeek: str
    openTime: datetime.time
    closeTime: datetime.time

    def __str__(self):
        return f"{self.dayOfWeek:<9} | {self.openTime} - {self.closeTime}"