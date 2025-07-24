import os
import django
import random
from faker import Faker
from django.conf import settings
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RecentCSCSTS.settings')  # Replace with your project's settings module
django.setup()

# Import models after django.setup()
from accounts.models import CustomUserProfile, EmployeeModel, VehicleModel

# Initialize Faker
fake = Faker()

def create_employees():
    employee_types = ['Manager', 'Technician', 'ServiceAdvisor', 'Receptionist']
    for tail in range(700, 800):
        username = f"{random.choice(employee_types)}{tail}"
        password = "Kamal@123"
        
        try:
            employee = EmployeeModel(
                username=username,
                full_name=fake.name()[:100],
                role=random.choice(employee_types)[:50],
                phone_number=fake.phone_number()[:15],
                address=fake.address()[:255],
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=65),
                profile_picture=None,  # Set to None to avoid ImageField issues
            )
            employee.set_password(password)
            employee.save()
            print(f"Created employee {username}")
        except Exception as e:
            print(f"Error creating employee {username}: {str(e)}")

def create_customer():
    User = get_user_model()
    for num in range(50, 100):
        username = f"Customer{num}"
        password = "Kamal@123"
        
        try:
            # Create the base User
            user = User.objects.create(
                username=username,
                first_name=fake.first_name()[:50],
                last_name=fake.last_name()[:50],
                email=fake.email()[:100],
            )
            user.set_password(password)
            user.save()

            # Create CustomUserProfile for the user
            profile = CustomUserProfile.objects.create(
                user=user,
                phone_number=fake.phone_number()[:15],
                address=fake.address()[:200],
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80),
                profile_picture=None
            )

            # Create a VehicleModel instance for the customer
            VehicleModel.objects.create(
                customer_id=profile,
                vin=fake.uuid4()[:17],
                chassis_number=fake.uuid4()[:50],  # Ensure unique chassis number
                reg_no=fake.license_plate()[:20],
                make=fake.company()[:50],
                model=f"VW{num}"[:50],
                year=random.randint(2000, 2023),
                mileage=random.randint(10000, 200000),
                colour=fake.color_name()[:50],
                trans=random.choice(['Auto', 'Manual']),
                image=None
            )
            print(f"Created customer {username}")
        except Exception as e:
            print(f"Error creating customer {username}: {str(e)}")

def main():
    print("Creating employees...")
    create_employees()
    print("Creating customers and vehicles...")
    create_customer()
    print("Data feeding completed.")

if __name__ == "__main__":
    main()