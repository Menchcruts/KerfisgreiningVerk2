from dataclasses import dataclass, field
import uuid


@dataclass
class AppointmentCategory:
    category_name: str = field(init=True)
    lengthInMinutes: int = field(init=True)
    minNumOfHoursBeforeCancellation: int = field(init=True)
    id: uuid.UUID = field(default_factory=uuid.uuid1)

    appointment_categories = []
 
    def __post_init__(self):
        if not isinstance(self.category_name, str) or not self.category_name:
            raise ValueError(f"{self.category_name} is not a non empty str")
        if not isinstance(self.lengthInMinutes, int) or self.lengthInMinutes <= 0:
            raise ValueError(f"{self.lengthInMinutes} is not a positive int")
        if not isinstance(self.minNumOfHoursBeforeCancellation, int) or self.minNumOfHoursBeforeCancellation < 0:
            raise ValueError(f"{self.minNumOfHoursBeforeCancellation} is not a non negative int")
        AppointmentCategory.appointment_categories.append(self)
        
    @classmethod
    def get_appointment_category_by_id(self, category_id: str):
        for category in AppointmentCategory.appointment_categories:
            if str(category.id) == category_id:
                return category
        return None
        

    def __str__(self):
        return f"{self.category_name} - {self.lengthInMinutes} minutes | Cancellation deadline: {self.minNumOfHoursBeforeCancellation} hours before"