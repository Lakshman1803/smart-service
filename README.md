# 🔧 SMART REPAIR — Vehicle Service Management System

**Premium vehicle service management platform for Andhra Pradesh**
Built with Django | Python | SQLite

---

## 🚀 QUICK SETUP (5 Minutes)

### Step 1: Install Python & Prerequisites
```bash
# Make sure Python 3.10+ is installed
python --version

# Install pip if not present
python -m ensurepip --upgrade
```

### Step 2: Set Up Virtual Environment
```bash
cd smart_repair
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Database Migrations
```bash
python manage.py makemigrations accounts
python manage.py makemigrations core
python manage.py makemigrations bookings
python manage.py makemigrations payments
python manage.py migrate
```

### Step 5: Seed Initial Data (AP Service Centers, Services, Employees)
```bash
python manage.py seed_data
```

### Step 6: Start the Server
```bash
python manage.py runserver
```

### Step 7: Open in Browser
```
http://127.0.0.1:8000/
```

---

## 🔑 DEFAULT LOGIN CREDENTIALS

### Admin Panel: http://127.0.0.1:8000/admin/
- Mobile: `9999999999`
- Password: `admin@123`

### Employee Login: http://127.0.0.1:8000/accounts/employee-login/
| Employee ID | Mobile     | Name           | Center        |
|-------------|------------|----------------|---------------|
| EMP001      | 8001000001 | Ravi Kumar     | Vijayawada    |
| EMP002      | 8001000002 | Suresh Reddy   | Vijayawada    |
| EMP003      | 8001000003 | Priya Sharma   | Vijayawada    |
| EMP004      | 8001000004 | Anand Krishna  | Visakhapatnam |
| EMP007      | 8001000007 | Venkat Rao     | Guntur        |

### Customer Login: http://127.0.0.1:8000/accounts/login/
- Enter any 10-digit mobile number
- OTP will be printed to the Django console (development mode)
- Check terminal for OTP: `[DEV] OTP for XXXXXXXXXX (login): 123456`

---

## 📋 FEATURES

### Customer Features
- ✅ OTP-based mobile login (no password needed)
- ✅ Register with mobile number + OTP verification
- ✅ Book service slot (online or offline/walk-in)
- ✅ Choose service center from 25+ AP locations shown on Google Maps
- ✅ Select from 2W / 3W / 4W / Heavy vehicle services
- ✅ Real-time service tracking with Booking ID
- ✅ SMS/notification when service is completed
- ✅ View and print payment receipts
- ✅ Online UPI payment with QR code
- ✅ 1-day advance reminder for service appointment

### Employee Features
- ✅ Login with Employee ID + Mobile Number (no OTP)
- ✅ Employee dashboard with live stats
- ✅ View and manage all center bookings
- ✅ OTP-verify customer before starting service
- ✅ Manually add customer vehicle data (walk-ins)
- ✅ Assign work to specific workers/technicians
- ✅ Mark service as complete → auto-notifies customer
- ✅ Generate itemized bill with extra charges
- ✅ Finalize payment (cash/online/UPI/card)
- ✅ Print professional receipt with "Have a Nice Day!"

### Admin Features
- ✅ Django admin panel for full control
- ✅ Add/edit service centers across AP
- ✅ Manage employees and designations
- ✅ Add service types with pricing
- ✅ Manage holiday calendar
- ✅ View all bookings and payments

---

## 🏢 SERVICE CENTERS (25+ across AP)

| City              | Centers | District          |
|-------------------|---------|-------------------|
| Vijayawada        | 6       | Krishna           |
| Visakhapatnam     | 4       | Visakhapatnam     |
| Guntur            | 3       | Guntur            |
| Tirupati          | 2       | Tirupati          |
| Amaravati         | 1       | Guntur            |
| Kurnool           | 1       | Kurnool           |
| Nellore           | 1       | SPSR Nellore      |
| Kakinada          | 1       | East Godavari     |
| Rajahmundry       | 1       | East Godavari     |
| Eluru             | 1       | West Godavari     |
| Ongole            | 1       | Prakasam          |
| Chittoor          | 1       | Chittoor          |
| Kadapa            | 1       | YSR Kadapa        |
| Srikakulam        | 1       | Srikakulam        |
| Vizianagaram      | 1       | Vizianagaram      |
| Bhimavaram        | 1       | West Godavari     |

---

## 🛠️ SERVICE CATEGORIES

| Vehicle Type      | Services Available                           |
|-------------------|----------------------------------------------|
| 🏍️ Two Wheeler   | Basic/Full Service, Tyre, Battery, Brake, Chain |
| 🛺 Three Wheeler  | Auto Service, CNG Kit, Tyre & Brake          |
| 🚗 Four Wheeler   | Car Service, AC, Denting, Alignment, Engine  |
| 🚛 Heavy Vehicle  | Truck/Bus Service, Engine Overhaul, Tyres    |
| 🔧 All Vehicles   | Wash, Detailing, Electrical, Emergency       |

---

## 💳 PAYMENT MODES

- **Cash** — Standard counter payment
- **Online UPI/QR** — Scan QR code → Pay → Enter UTR reference
- **Card** — Debit/Credit card at counter
- **Net Banking** — Online banking transfer

---

## 📱 SMS / OTP INTEGRATION

For production, integrate one of these SMS providers:

### Fast2SMS (Recommended for India)
1. Sign up at https://www.fast2sms.com
2. Get API key
3. In `smart_repair/settings.py`, set `SMS_API_KEY = 'your-key'`
4. Uncomment the SMS code in `accounts/views.py` → `send_otp()` function

### Twilio
1. Sign up at https://www.twilio.com
2. Get Account SID, Auth Token, Phone Number
3. `pip install twilio`
4. Update `send_otp()` in `accounts/views.py`

**Development Mode:** OTP is printed to Django console — check terminal!

---

## 🗺️ GOOGLE MAPS INTEGRATION

1. Get API key from https://console.cloud.google.com
2. Enable: Maps JavaScript API, Places API, Geocoding API
3. In `smart_repair/settings.py`, set `GOOGLE_MAPS_API_KEY = 'your-key'`

---

## 📁 PROJECT STRUCTURE

```
smart_repair/
├── manage.py
├── requirements.txt
├── README.md
├── smart_repair/
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL router
│   └── wsgi.py
├── core/                    # Service centers, services, holidays
│   ├── models.py            # ServiceCenter, ServiceType, Holiday
│   ├── views.py             # Home, centers, track, contact
│   ├── urls.py
│   └── management/commands/
│       └── seed_data.py     # Data seeding command
├── accounts/                # Users, employees, OTP
│   ├── models.py            # User, Employee, OTPVerification
│   ├── views.py             # Login, register, dashboard
│   └── urls.py
├── bookings/                # Slot booking, service records
│   ├── models.py            # Booking, Vehicle, TimeSlot
│   ├── views.py             # Book, assign, complete
│   └── urls.py
├── payments/                # Billing and receipts
│   ├── models.py            # Payment, ServiceCharge
│   ├── views.py             # Bill, receipt, online payment
│   └── urls.py
├── static/
│   └── css/style.css        # Stylesheet
├── templates/
│   ├── base.html            # Base layout with navbar/footer
│   ├── core/                # Home, centers, services, track
│   ├── accounts/            # Login, register, dashboard
│   ├── bookings/            # Booking flow templates
│   ├── payments/            # Receipt, billing templates
│   └── errors/              # 404, 500 pages
└── media/                   # User uploads
```

---

## 🎨 OPEN IN SUBLIME TEXT

1. Open Sublime Text
2. File → Open Folder → Select `smart_repair/`
3. Recommended packages: `Python`, `Django Syntax`, `SublimeLinter`

---

## ⚠️ TROUBLESHOOTING

**Import Error:** Run `pip install -r requirements.txt` again

**Migration Error:** Delete `db.sqlite3` and all `migrations/` folders except `__init__.py`, then re-run migrations

**OTP not received:** Check Django console/terminal — OTP is printed there in dev mode

**Static files not loading:** Run `python manage.py collectstatic`

**No time slots showing:** Run `python manage.py seed_data` to create slots for the next 14 days

---

## 📞 SUPPORT

- Email: info@smartrepair.in
- Phone: +91-9876543210
- Working: Monday to Saturday, 8 AM – 7 PM

---

*SMART REPAIR — Have a Nice Day! 🙏*
