import uuid
from .AppointmentCategory import AppointmentCategory
from .BusinessHours import BusinessHours


class Business:
    def __init__(self, Name:str):
        self.id: uuid.UUID = uuid.uuid1()
        
        assert isinstance(Name, str)
        self.name: str = Name
        
        self.appointmentCategories: list[AppointmentCategory]    = []
        self.businessHours: list[BusinessHours]                  = []

    def addAppointmentCategory(self, category: AppointmentCategory) -> bool:
        if not isinstance(category, AppointmentCategory):
            raise ValueError(f"{type(category)} is not of value {AppointmentCategory.__name__}")
        self.appointmentCategories.append(category)

    def addBusinessHours(self, hours: BusinessHours) -> bool:
        if not isinstance(hours, BusinessHours):
            raise ValueError(f"{type(category)} is not of value {BusinessHours.__name__}")
        self.businessHours.append(hours)
