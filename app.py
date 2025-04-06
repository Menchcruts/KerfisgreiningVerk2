from flask import Flask, request, jsonify, abort
from src.models.User import User
from src.models.Business import Business
from src.models.AppointmentCategory import AppointmentCategory
from src.models.Booking import Booking
from src.models.BusinessHours import BusinessHours
from src.services.BookingService import BookingService
from datetime import datetime, timedelta

app = Flask(__name__)


businesses = {}
users = {}
bookings = {}

@app.route('/register_user', methods=['POST'])
def register_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    
    if not name or not email:
        abort(400, 'Name and email are required')
        
    try:
        new_user = User(name=name, email=email)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'message': 'User registered successfully',
                    'user': {
                        'id': str(new_user.id),
                        'name': new_user.name
                        }
                    }), 201

@app.route('/create_business', methods=['POST'])
def create_business():
    data = request.json 
    business_name = data.get('business_name')
    
    if not business_name:
        abort(400, 'Name is required')
        
    try:
        new_business = Business(business_name=business_name)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'message': 'Business created successfully', 
                    "business":{
                        'id': str(new_business.id), 
                        'business_name': new_business.business_name
                        }
                    }), 201

@app.route('/add_appointment_category/<business_id>', methods=['POST'])
def add_appointment_category(business_id):
    data = request.json 
    category_name = data.get('category_name')
    if not category_name:
        return jsonify({'error': 'Category name is required'}), 400

    lengthInMinutes = data.get('lengthInMinutes')
    minNumOfHoursBeforeCancellation = data.get('minNumOfHoursBeforeCancellation')
    
    if lengthInMinutes is None or minNumOfHoursBeforeCancellation is None:
        abort(400, 'lengthInMinutes and minNumOfHoursBeforeCancellation are required')

    business = businesses.get(str(business_id))
        
    if not business:
        return jsonify({'error': 'Business not found'}), 404
    
    try:
        new_category = AppointmentCategory(category_name=category_name, minNumOfHoursBeforeCancellation=data.get('minNumOfHoursBeforeCancellation'), lengthInMinutes=data.get('lengthInMinutes'))
        business.addAppointmentCategory(new_category)
    except ValueError as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'message': 'Appointment category added successfully',
                    'category': {
                        'name': new_category.category_name,
                        'id': str(new_category.id)
                    }}), 201

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    data = request.json
    user_id = data.get('user_id')
    business_id = data.get('business_id')
    appointment_category_id = data.get('appointment_category_id')
    scheduled_time = data.get('scheduled_time')
    
    user = users.get(str(user_id))
    if not user:
        abort(404, "User not found.")

    business = businesses.get(business_id)
    if not business:
        abort(404, "Business not found.")
    
    appointment_category = None
    for ac in appointment_category:
        if str(ac.id) == appointment_category_id:
            appointment_category = ac
            break
    
    if not user_id or not business_id or not appointment_category_id or not scheduled_time:
        abort(400, 'User ID, business ID, appointment category ID and scheduled time are required')

    try:
        scheduled_time = datetime.fromisoformat(scheduled_time)
    except ValueError:
        abort(400, 'Invalid scheduled time format. Use ISO format (YYYY-MM-DDTHH:MM:SS)')
    if scheduled_time < datetime.now():
        abort(400, 'Scheduled time must be in the future') 
        
    appointment_category = AppointmentCategory.get_appointment_category_by_id(str(appointment_category_id))
    if not appointment_category:
        abort(404, 'Appointment category not found')
        
    booking = Booking(user_id, Start = scheduled_time, End = scheduled_time + timedelta(minutes=appointment_category.lengthInMinutes), Category = appointment_category)
    bookings.append(booking)
    return jsonify({'message': 'Appointment booked successfully', "booking": str(booking), 'for user': str(user_id)}), 201

@app.route('/get_user_bookings/<user_id>', methods=['GET'])
def get_user_bookings(user_id):    
    user = users.get(user_id)
    if not user:
        abort(404, 'User not found')
    
    user_bookings = [
        {
        'id': str(booking.id),
        'scheduled_start_time': booking.scheduledStartTime,
        'scheduled_end_time': booking.scheduledEndTime,
        }
        for booking in bookings if booking.user_id == user.id and booking.scheduledStartTime >= datetime.now()
        ]
    if not user_bookings:
        return jsonify({'message': 'No upcoming bookings found'}), 404
    return jsonify({'bookings': user_bookings}), 200

if __name__ == '__main__':
    app.run(debug=True)