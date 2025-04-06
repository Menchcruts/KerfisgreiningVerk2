import unittest
import json 
from app import app 

class APITests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        self.app.application.users = []
        self.app.application.businesses = []
        self.app.application.bookings = []
        
        
    def test_register_user(self):
        response = self.app.post('/register_user', json={'name': 'John Doe', 'email': 'john@x.com'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', str(response.data))
        
    def test_register_user_missing_fields(self):
        response = self.app.post('/register_user', json={'name': 'John Doe'})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Name and email are required', str(response.data))
        
    def test_create_business(self):
        self.app.post('/register_user', json={'name': 'John Doe', 'email': 'john@x.com'})
        response = self.app.post('/create_business', json={'business_name': 'Hair by Me'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Business created successfully', str(response.data))
        
        
    def test_create_business_missing_fields(self):
        response = self.app.post('/create_business', json={})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Name is required', str(response.data))
        
    def test_add_appointment_category(self):
        self.app.post('/register_user', json={'name': 'John Doe', 'email': 'john@x.com'})
        response = self.app.post('/create_business', json={'business_name': 'Hair by Me'})
        business_id = response.json['business']['id']
        response = self.app.post(f'/add_appointment_category/{business_id}', json={'category_name': 'haircut', 'lengthInMinutes': 30, 'minNumOfHoursBeforeCancellation': 24})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Appointment category added successfully', str(response.data))
        
    def test_add_appointment_category_business_not_found(self):
        business_id = None
        response = self.app.post(f'/add_appointment_category/{business_id}', json={'category_name': 'haircut', 'lengthInMinutes': 30, 'minNumOfHoursBeforeCancellation': 24})
        self.assertEqual(response.status_code, 404)
        self.assertIn('Business not found', str(response.data))
        
    def test_book_appointment(self):
        self.app.post('/register_user', json={'name': 'John Doe', 'email': 'john@x.com'})
        response = self.app.post('/create_business', json={'business_name': 'Hair by Me'})
        business_id = response.json['business']['id']
        response = self.app.post(f'/add_appointment_category/{business_id}', json={'category_name': 'haircut', 'lengthInMinutes': 30, 'minNumOfHoursBeforeCancellation': 24})
        appointment_category_id = response.json['category']['id']
        response = self.app.post('/book_appointment', json={'userId': 1, 'businessId': business_id, 'appointmentCategoryId': appointment_category_id, 'scheduledTime': '2025-10-01T10:00:00'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Appointment booked successfully', str(response.data))
      
    def test_book_appointment_missing_fields(self):
        response = self.app.post('/book_appointment', json={'userId': 1, 'businessId': 1})
        self.assertEqual(response.status_code, 400)
        self.assertIn('User ID, business ID, appointment category ID and scheduled time are required', str(response.data))
    
    def test_get_user_bookings(self):
        response = self.app.post('/register_user', json={'name': 'John Doe', 'email': 'john@x.com'})
        user_id = response.json['user']['id']
        
        response = self.app.post('/create_business', json={'business_name': 'Hair by Me'})
        business_id = response.json['business']['id']
        
        response = self.app.post(f'/add_appointment_category/{business_id}', json={
                                    'category_name': 'haircut',
                                    'lengthInMinutes': 30,
                                    'minNumOfHoursBeforeCancellation': 24
                                })
        appointment_category_id = response.json['category']['id']

        response = self.app.post('/book_appointment', json={
                                    'userId': user_id,
                                    'businessId': business_id,
                                    'appointmentCategoryId': appointment_category_id,
                                    'scheduledTime': '2025-10-01T10:00:00'
                                })

        response = self.app.get(f'/get_user_bookings/{user_id}')  

        self.assertEqual(response.status_code, 200)  
        self.assertIn('bookings', str(response.data))
        
    if __name__ == '__main__':
        unittest.main()