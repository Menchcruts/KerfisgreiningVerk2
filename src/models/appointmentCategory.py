class AppointmentCategory:
    def __init__(self, category_id: int, name: str, length_in_minutes: int, min_hours_before_cancellation: int):
        self.category_id = category_id
        self.name = name
        self.length_in_minutes = length_in_minutes
        self.min_hours_before_cancellation = min_hours_before_cancellation

    def __repr__(self):
        return f"AppointmentCategory(id={self.category_id}, name='{self.name}', length={self.length_in_minutes}m, cancel={self.min_hours_before_cancellation}h)"
