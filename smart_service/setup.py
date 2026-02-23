"""
setup.py - Run this to initialize the database with sample data.
Usage: python setup.py (from project root)
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_service.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth.models import User
from service_app.models import Employee, Worker

print("\n" + "="*60)
print("  SMART SERVICE - Initial Setup")
print("="*60)

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@smartservice.in', 'admin123')
    print("✅ Superuser created: admin / admin123")
else:
    print("ℹ️  Superuser already exists")

# Create sample employees
employees_data = [
    {'employee_id': 'EMP001', 'name': 'Rajesh Kumar', 'mobile': '9876543210', 'role': 'Service Advisor'},
    {'employee_id': 'EMP002', 'name': 'Priya Sharma', 'mobile': '9876543211', 'role': 'Service Advisor'},
    {'employee_id': 'EMP003', 'name': 'Suresh Babu', 'mobile': '9876543212', 'role': 'Senior Technician'},
]

print("\n--- Employees ---")
for emp in employees_data:
    obj, created = Employee.objects.get_or_create(
        employee_id=emp['employee_id'],
        defaults=emp
    )
    status = "✅ Created" if created else "ℹ️  Exists"
    print(f"  {status}: {obj.employee_id} - {obj.name} (Mobile: {obj.mobile})")

# Create workers
workers_data = [
    {'name': 'Raju', 'specialization': 'Engine & Mechanical'},
    {'name': 'Sai', 'specialization': 'Electricals & AC'},
    {'name': 'Charan', 'specialization': 'Body Work & Painting'},
    {'name': 'Mahesh', 'specialization': 'Tyre & Wheel Alignment'},
    {'name': 'Subbu', 'specialization': 'General Service & Oil'},
    {'name': 'Venkat', 'specialization': 'Brake & Suspension'},
    {'name': 'Arun', 'specialization': 'Detailing & Wash'},
]

print("\n--- Workers ---")
for w in workers_data:
    obj, created = Worker.objects.get_or_create(name=w['name'], defaults=w)
    status = "✅ Created" if created else "ℹ️  Exists"
    print(f"  {status}: {obj.name} ({obj.specialization})")

print("\n" + "="*60)
print("  Setup Complete!")
print("="*60)
print("\n📌 HOW TO RUN THE PROJECT:")
print("  1. pip install django")
print("  2. python manage.py migrate")
print("  3. python setup.py  (run this file)")
print("  4. python manage.py runserver")
print("  5. Visit: http://127.0.0.1:8000/")
print("\n🔐 EMPLOYEE LOGIN CREDENTIALS:")
for emp in employees_data:
    print(f"  ID: {emp['employee_id']} | Mobile: {emp['mobile']}")
print("\n👤 ADMIN PANEL: http://127.0.0.1:8000/admin/")
print("  Username: admin | Password: admin123")
print("\n📱 OTP MODE: In development, OTPs are printed to this terminal.")
print("="*60 + "\n")
