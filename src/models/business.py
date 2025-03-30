class Business:
    def __init__(self, business_id: int, name: str):
        self.business_id = business_id
        self.name = name
        self.appointment_categories = []  
        self.business_hours = []  

    def add_appointment_category(self, category):
        if isinstance(category, AppointmentCategory):
            self.appointment_categories.append(category)
            return True
        return False

    def add_business_hours(self, hours):
        if isinstance(hours, BusinessHours):
            self.business_hours.append(hours)
            return True
        return False

    def __repr__(self):
        return f"Business(id={self.business_id}, name='{self.name}')"