from flask import Flask, request, jsonify, abort
from src.models.User import User
from src.models.Business import Business
from src.models.AppointmentCategory import AppointmentCategory
from src.models.Booking import Booking
from src.models.BusinessHours import BusinessHours
from src.services.BookingService import BookingService
from datetime import datetime, time
from uuid import UUID

app = Flask(__name__)


businesses:dict[str, Business] = {}
users:dict[str, User] = {}
service = BookingService()

@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        abort(400, 'Name and email are required')
        
    user = User(name=name, email=email)
    users[email] = user
    return jsonify({'message': 'User registered successfully',
                    "user": {
                        'id': str(user.id),
                        'name': user.name,
                        'email': user.email,
                        }
                    }), 201

@app.route('/create_business', methods=['POST'])
def create_business():
    data = request.json 
    name = data.get('name')
    
    if not name:
        abort(400, 'Name is required')
        
    business = Business(name=name)
    businesses[name] = business
    business_hours = BusinessHours(dayOfWeek="Monday", openTime=time(8, 0), closeTime=time(17, 0))
    business.addBusinessHours(business_hours)
    business_hours = BusinessHours(dayOfWeek="Tuesday", openTime=time(8, 0), closeTime=time(17, 0))
    business.addBusinessHours(business_hours)
    business_hours = BusinessHours(dayOfWeek="Wednesday", openTime=time(8, 0), closeTime=time(17, 0))
    business.addBusinessHours(business_hours)
    business_hours = BusinessHours(dayOfWeek="Thursday", openTime=time(8, 0), closeTime=time(17, 0))
    business.addBusinessHours(business_hours)
    business_hours = BusinessHours(dayOfWeek="Friday", openTime=time(8, 0), closeTime=time(17, 0))
    business.addBusinessHours(business_hours)
    return jsonify({'message': 'Business created successfully', 
                    "business": {
                        'id': str(business.id),
                        'name': business.name,
                        }
                    }), 201

@app.route('/add_appointment_category/<business_name>', methods=['POST'])
def add_appointment_category(business_name):
    data = request.json 
    name = data.get('name')
    lengthInMinutes = data.get('lengthInMinutes')
    minNumOfHoursBeforeCancellation = data.get('minNumOfHoursBeforeCancellation')
    business = businesses.get(business_name)
    if not business:
        abort(404, 'Business not found')
    
    if not name or lengthInMinutes is None or minNumOfHoursBeforeCancellation is None:
        abort(400, 'Name, lengthInMinutes and minNumOfHoursBeforeCancellation are required')
        
    
            
    appointment_category = AppointmentCategory(name=name, lengthInMinutes=lengthInMinutes, minNumOfHoursBeforeCancellation=minNumOfHoursBeforeCancellation)
    business.addAppointmentCategory(appointment_category)
    return jsonify({'message': 'Appointment category added successfully', 
                    "appointment_category": {
                        'id': str(appointment_category.id),
                        'name': appointment_category.name,
                        'lengthInMinutes': appointment_category.lengthInMinutes,
                        'minNumOfHoursBeforeCancellation': appointment_category.minNumOfHoursBeforeCancellation,   
                        }
                    }), 201

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    data = request.json
    user_id = data.get('user_id')
    business_name = data.get('business_name')
    appointment_category_id = data.get('appointmentCategoryId')
    scheduled_time = data.get('scheduledTime')
    
    if not user_id:
        abort(404, "User not found.")

    if not business_name:
        abort(404, "Business not found.")
    
    business = businesses.get(business_name)
    
    for category in business.appointmentCategories:
        if str(category.id) == appointment_category_id:
            appointment_category = category
            break
        else:
            abort(400, 'Appointment category is required')
        
    
    scheduled_time = datetime.fromisoformat(scheduled_time)
    if not BookingService.isAvailableForBooking(business, appointment_category, scheduled_time):
        abort(400, 'Time slot is not available')

    booking = service.createBooking(user_id, appointment_category, scheduled_time)
    return jsonify({'message': 'Appointment booked successfully', "booking": str(booking)}), 201

@app.route('/get_user_bookings/<user_id>', methods=['GET'])
def get_user_bookings(user_id):
    if not user_id:
        abort(404, 'User not found')
        
    user_bookings = service.getBookingsForUser(user_id)
    bookings_dict = [booking.to_dict() for booking in user_bookings]
    return jsonify({'bookings': bookings_dict}), 200

if __name__ == '__main__':
    app.run(debug=True)