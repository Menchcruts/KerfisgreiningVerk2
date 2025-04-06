import uuid
from .AppointmentCategory import AppointmentCategory
from .BusinessHours import BusinessHours


class Business:
    businesses = []
    def __init__(self, business_name: str):
        self.id: uuid.UUID = uuid.uuid1()
        
        assert isinstance(business_name, str)
        self.business_name: str = business_name
        
        self.appointmentCategories: list[AppointmentCategory]    = []
        self.businessHours: list[BusinessHours]                  = []
        
        Business.businesses.append(self) 
        
    @classmethod
    def get_business_by_id(self, business_id: str):
        for business in Business.businesses:
            if str(business.id) == business_id:
                return business
            
    def addAppointmentCategory(self, category: AppointmentCategory) -> bool:
        if not isinstance(category, AppointmentCategory):
            raise ValueError(f"{type(category)} is not of value {AppointmentCategory.__name__}")
        self.appointmentCategories.append(category)
        return True

    def addBusinessHours(self, hours: BusinessHours) -> bool:
        if not isinstance(hours, BusinessHours):
            raise ValueError(f"{type(hours)} is not of value {BusinessHours.__name__}")
        self.businessHours.append(hours)
        return True
