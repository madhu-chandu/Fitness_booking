# Fitness_booking
# 🏋️‍♀️ Fitness Class Booking API (Django)

This is a backend-only Django application that allows a fictional fitness studio to manage classes like **Yoga**, **Zumba**, and **HIIT**, and enables clients to view, book, and track their bookings.

---

## ✅ Features

- View upcoming classes with slots
- Book available classes
- Get bookings by email
- Handles timezones (IST default)
- Prevents overbooking
- SQLite for storage
- Input validation and error handling
- Logging for each booking

---

## 🛠 Tech Stack

- Python 3.x
- Django
- Django REST Framework
- SQLite
- Pytz (timezone management)

---

## 🚀 Setup Instructions

```bash
# Step 1: Clone project
git clone https://github.com/your-username/fitness-booking.git
cd fitness-booking

# Step 2: Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Step 3: Install dependencies
pip install django djangorestframework pytz

# Step 4: Run migrations
python manage.py makemigrations
python manage.py migrate

# Step 5: Create admin user (optional)
python manage.py createsuperuser

# Step 6: Start the server
python manage.py runserver
🔗 API Endpoints
1. 📅 View All Available Classes
GET /api/classes/

Returns all upcoming classes with their details.

Example Request:

bash
Copy
Edit
curl http://127.0.0.1:8000/api/classes/
Response:

json
Copy
Edit
[
  {
    "id": 1,
    "name": "Yoga",
    "instructor": "Asha",
    "datetime": "2025-06-08T08:00:00+05:30",
    "available_slots": 10
  },
  {
    "id": 2,
    "name": "Zumba",
    "instructor": "Ravi",
    "datetime": "2025-06-08T10:00:00+05:30",
    "available_slots": 5
  }
]
2. 🧾 Book a Class
POST /api/book/

Creates a booking only if slots are available.

Body (JSON):

json
Copy
Edit
{
  "class_id": 1,
  "client_name": "John",
  "client_email": "john@example.com"
}
Example Request:

bash
Copy
Edit
curl -X POST http://127.0.0.1:8000/api/book/ \
-H "Content-Type: application/json" \
-d "{\"class_id\": 1, \"client_name\": \"John\", \"client_email\": \"john@example.com\"}"
Response:

json
Copy
Edit
{
  "id": 1,
  "fitness_class": 1,
  "client_name": "John",
  "client_email": "john@example.com",
  "booked_at": "2025-06-06T21:42:10.123456Z"
}
3. 📩 Get All Bookings by Email
GET /api/bookings/?email=john@example.com

Returns bookings made by that client.

Example Request:

bash
Copy
Edit
curl "http://127.0.0.1:8000/api/bookings/?email=john@example.com"
Response:

json
Copy
Edit
[
  {
    "id": 1,
    "fitness_class": 1,
    "client_name": "John",
    "client_email": "john@example.com",
    "booked_at": "2025-06-06T21:42:10.123456Z"
  }
]
🧪 Seed Class Data (Optional)
Add classes via Django Admin (/admin) or use this snippet in the Django shell:

python
Copy
Edit
from studio.models import FitnessClass
from django.utils.timezone import make_aware
from datetime import datetime

FitnessClass.objects.create(
    name='Yoga',
    instructor='Asha',
    datetime=make_aware(datetime(2025, 6, 8, 8, 0)),
    available_slots=10
)
🧠 Notes
All class times are stored in IST by default.

Use the admin panel to manage classes.

Responses are in JSON.

Overbooking returns appropriate error message.

Missing fields return validation errors.

💡 Logging & Validation
All booking requests are logged.

Missing fields, invalid class IDs, or 0 slots return 400 or 404 error.

Bookings are only created if slots are available.
