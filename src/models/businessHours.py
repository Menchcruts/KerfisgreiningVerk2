class BusinessHours:
    def __init__(self, hours_id: int, day_of_week: str, open_time: str, close_time: str):
        self.hours_id = hours_id
        self.day_of_week = day_of_week
        self.open_time = open_time  
        self.close_time = close_time  

    def __repr__(self):
        return f"BusinessHours(id={self.hours_id}, day='{self.day_of_week}', open={self.open_time}, close={self.close_time})"
