from dataclasses import dataclass, field
import datetime
import uuid

@dataclass
class BusinessHours:
    id: uuid.UUID = field(default_factory=uuid.uuid1, init=False)
    dayOfWeek: str
    openTime: datetime.time
    closeTime: datetime.time
    
    def __init__(self, opening_time: str, closing_time: str, day_of_week: str):
        # Validate day of the week
        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if day_of_week not in valid_days:
            raise ValueError(f"{day_of_week} is not a valid day of the week. Choose from {valid_days}")
        
        # Validate time format
        try:
            self.openTime = datetime.datetime.strptime(opening_time, '%H:%M').time()
            self.closeTime = datetime.datetime.strptime(closing_time, '%H:%M').time()
        except ValueError:
            raise ValueError("Time must be in HH:MM format")
        
        if self.openTime >= self.closeTime:
            raise ValueError(f"Opening time {opening_time} must be before closing time {closing_time}")
        
        self.dayOfWeek = day_of_week
        
    def within_hours(self, scheduled_time: datetime) -> bool:
        # Check if the scheduled time is within the business hours
        scheduled_time = scheduled_time.time()
        return self.openTime <= scheduled_time <= self.closeTime

    def __str__(self):
        # Left justifies the day by the length of 'Wednesday'
        return f"{self.dayOfWeek:<9} | {self.openTime} - {self.closeTime}"