from flask import Flask, request, jsonify, abort
from src.models.User import User
from src.models.Business import Business
from src.models.AppointmentCategory import AppointmentCategory
from src.models.Booking import Booking
from src.models.BusinessHours import BusinessHours
from src.services.BookingService import BookingService
from datetime import datetime, timedelta

app = Flask(__name__)


businesses = []
users = []
bookings = []

@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.json 
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        abort(400, 'Name and email are required')
        
    user = User(name=name, email=email)
    users.append(user)
    return jsonify({'message': 'User registered successfully', "user": str(user)}), 201

@app.route('/create_business', methods=['POST'])
def create_business():
    data = request.json 
    name = data.get('name')
    
    if not name:
        abort(400, 'Name is required')
        
    business = Business(name=name)
    businesses.append(business)
    return jsonify({'message': 'Business created successfully', "business": str(business)}), 201

@app.route('/add_appointment_category/<business_id>', methods=['POST'])
def add_appointment_category(business_id):
    data = request.json 
    name = data.get('name')
    lengthInMinutes = data.get('lengthInMinutes')
    minNumOfHoursBeforeCancellation = data.get('minNumOfHoursBeforeCancellation')
    
    if not name or lengthInMinutes is None or minNumOfHoursBeforeCancellation is None:
        abort(400, 'Name, lengthInMinutes and minNumOfHoursBeforeCancellation are required')
        
    business = None
    for b in business:
        if str(b.id) == business_id:
            business = b
            break
    if not business:
        abort(404, 'Business not found')
            
    appointment_category = AppointmentCategory(name=name, lengthInMinutes=lengthInMinutes, minNumOfHoursBeforeCancellation=minNumOfHoursBeforeCancellation)
    business.addAppointmentCategory(appointment_category)
    return jsonify({'message': 'Appointment category added successfully', "appointment_category": str(appointment_category)}), 201

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    data = request.json
    user_id = data.get('user_id')
    business_id = data.get('business_id')
    appointment_category_id = data.get('appointment_category_id')
    scheduled_time = data.get('scheduled_time')
    
    user = None
    for u in users:
        if str(u.id) == user_id:
            user = u
            break
        
    business = None
    for b in business:
        if str(b.id) == business_id:
            business = b
            break
        
    appointment_category = None
    for ac in appointment_category:
        if str(ac.id) == appointment_category_id:
            appointment_category = ac
            break
    
    if not user or not business or not appointment_category:
        abort(400, 'User, business and appointment category are required')
        
    scheduled_time = datetime.fromisoformat(scheduled_time)
    if not BookingService.isAvailableForBooking(business, appointment_category, scheduled_time):
        abort(400, 'Time slot is not available')
        
    booking = Booking(Start = scheduled_time, End = scheduled_time + timedelta(minutes=appointment_category.lengthInMinutes), Category = appointment_category)
    bookings.append(booking)
    return jsonify({'message': 'Appointment booked successfully', "booking": str(booking)}), 201

@app.route('/get_user_bookings/<user_id>', methods=['GET'])
def get_user_bookings(user_id):
    user = None
    for u in users:
        if str(u.id) == user_id:
            user = u
            break
    if not user:
        abort(404, 'User not found')
        
    user_bookings = [str(booking) for booking in bookings if booking.scheduledStartTime >= datetime.now()]
    return jsonify({'bookings': user_bookings}), 200

if __name__ == '__main__':
    app.run(debug=True)