# 🚗 SMART SERVICE - Vehicle Service Management System

A complete Django-based vehicle service management system for 2, 3, and 4-wheelers.

---

## 🚀 Quick Setup (5 Steps)

### Step 1: Install Python & Django
```bash
pip install django pillow
```

### Step 2: Set up the project
```bash
cd smart_service
python manage.py migrate
```

### Step 3: Run setup script (creates employees, workers, admin)
```bash
python setup.py
```

### Step 4: Start the server
```bash
python manage.py runserver
```

### Step 5: Open in browser
```
http://127.0.0.1:8000/
```

---

## 🔐 Login Credentials

### Employee Logins (created by setup.py):
| Employee ID | Mobile     | Name          | Role             |
|-------------|------------|---------------|------------------|
| EMP001      | 9876543210 | Rajesh Kumar  | Service Advisor  |
| EMP002      | 9876543211 | Priya Sharma  | Service Advisor  |
| EMP003      | 9876543212 | Suresh Babu   | Senior Technician|

### Admin Panel:
- URL: `http://127.0.0.1:8000/admin/`
- Username: `admin`
- Password: `admin123`

### Customer Login:
- Any 10-digit mobile number → OTP sent
- **In development mode**: OTP is printed in the terminal!

---

## 📱 OTP Mode

By default, OTPs are printed in the terminal (console mode). To use real SMS:

1. Sign up for [Twilio](https://twilio.com)
2. Edit `smart_service/settings.py`:
```python
SMS_BACKEND = 'twilio'
TWILIO_ACCOUNT_SID = 'your_sid'
TWILIO_AUTH_TOKEN = 'your_token'
TWILIO_PHONE_NUMBER = '+1234567890'
```
3. `pip install twilio`

---

## 📂 Project Structure

```
smart_service/
├── manage.py
├── setup.py                    # Run this for initial data
├── db.sqlite3                  # Created after migrate
├── smart_service/
│   ├── settings.py
│   └── urls.py
└── service_app/
    ├── models.py               # All database models
    ├── views.py                # All page logic
    ├── urls.py                 # URL routing
    ├── admin.py                # Admin panel config
    ├── utils.py                # OTP generation & sending
    └── templates/service_app/
        ├── base.html           # Navigation & footer
        ├── home.html           # Main landing page
        ├── customer_login.html
        ├── employee_login.html
        ├── otp_verify.html     # OTP input with timer
        ├── customer_dashboard.html
        ├── employee_dashboard.html
        ├── add_service.html    # New service request form
        ├── assign_work.html    # Assign workers
        ├── payment.html        # Payment processing
        ├── receipt.html        # Printable receipt
        ├── track.html          # Service tracking
        └── 404.html            # Custom error page
```

---

## 🛠️ Features

### 🏠 Home Page
- Hero section with SMART SERVICE branding
- Stats bar (customers, vehicles, experience)
- All services listed with icons
- Vehicle gallery (2W, 3W, 4W) with real images from Unsplash
- Service tracking widget
- Contact information
- Login/Register options

### 👤 Customer Flow
1. Enter mobile number → receive OTP
2. Verify OTP → auto-register if new user
3. Complete profile (name, email, address)
4. View service history & notifications
5. Track any service with tracking ID
6. Receive SMS notifications on service updates

### 🔧 Employee Flow
1. Login with Employee ID + Mobile Number
2. Add new service request (customer + vehicle details)
3. OTP sent to customer for acceptance
4. Assign work to workers (Raju, Sai, Charan, Mahesh, Subbu, etc.)
5. Update service status (Pending → Accepted → In Progress → Completed)
6. Process payment (Cash / UPI / Card / Online)
7. Generate and print receipt

### 💳 Payment
- Cash/Offline payment
- UPI payment
- Card payment
- Online transfer
- Auto-generated receipt with receipt number
- Notification sent to customer after payment

### 📊 Database Models
- `Employee` - Staff with employee ID & mobile
- `Customer` - Customer profiles
- `Vehicle` - 2W/3W/4W vehicles
- `ServiceRequest` - Service jobs with tracking ID
- `WorkAssignment` - Tasks assigned to workers
- `Payment` - Payment records
- `Notification` - Customer alerts
- `OTP` - OTP management with expiry

---

## 🎨 Tech Stack
- **Backend**: Django 4.x (Python)
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Frontend**: HTML, CSS, Vanilla JS
- **Icons**: Font Awesome 6
- **Fonts**: Orbitron, Poppins (Google Fonts)
- **SMS**: Console (dev) / Twilio (prod)

---

## 📝 Adding More Employees

Via Admin Panel:
1. Go to `/admin/`
2. Click `Employees` → `Add Employee`
3. Fill in Employee ID, Name, Mobile, Role

Via Django Shell:
```python
python manage.py shell
from service_app.models import Employee
Employee.objects.create(employee_id='EMP004', name='New Employee', mobile='9999999999', role='Technician')
```

---

## 🌐 Production Deployment
1. Set `DEBUG = False` in settings.py
2. Set a strong `SECRET_KEY`
3. Configure PostgreSQL database
4. Set up Twilio for real SMS
5. Run `python manage.py collectstatic`
6. Deploy on Heroku, Railway, or VPS
