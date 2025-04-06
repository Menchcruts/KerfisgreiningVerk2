import uuid
from .AppointmentCategory import AppointmentCategory
from .User import User
from datetime import datetime, timedelta

class Booking:
    def __init__(self, user:User, Start:datetime, End:datetime, Category:AppointmentCategory):
        self.id: uuid.UUID = uuid.uuid1()
        self.user = user

        assert isinstance(Start, datetime)
        assert isinstance(End, datetime)
        assert isinstance(Category, AppointmentCategory)

        self.scheduledStartTime: datetime = Start
        self.scheduledEndTime: datetime = End

        self.appointmentCategory: AppointmentCategory = Category
        self.cancellationDeadline: datetime = self.calculateCancellationDeadline()

    def calculateCancellationDeadline(self) -> datetime:
        min_hours = self.appointmentCategory.minNumOfHoursBeforeCancellation
        deadline = self.scheduledStartTime - timedelta(hours=min_hours)
        return deadline

    def canBeCancelled(self) -> bool:
        return datetime.now() < self.cancellationDeadline