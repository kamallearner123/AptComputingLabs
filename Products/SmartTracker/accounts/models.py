from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.html import format_html
from .constants import ROLE_CHOICES, STATUS_CHOICES
import random
from django.contrib.auth import get_user_model


# Create your models here.


class EmployeeModel(AbstractUser):
    #user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    # Prefix settings.MEDIA_DIR for media files

    profile_picture = models.ImageField(upload_to='employee_profile_pictures', blank=True, null=True)
    
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.role})"

    class Meta:
        db_table = 'accounts_employeemodel'  # Optional, only if explicitly set

class CustomUserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='user_profile_pictures', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Profile"

    class Meta:
        db_table = 'accounts_customuserprofile'

class VehicleModel(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(CustomUserProfile, on_delete=models.CASCADE, related_name='vehicles')
    
    # Include Chassis Number, it is a unique identifier for the vehicle
    chassis_number = models.CharField(max_length=50, unique=True)
    reg_no = models.CharField(max_length=20, unique=True)

    # Existing Fields
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    vin = models.CharField(max_length=17, unique=True)

    # New Fields from Form
    colour = models.CharField(max_length=50, default='Unknown')
    mileage = models.PositiveIntegerField()
    trans = models.CharField(max_length=10, choices=[('Auto', 'Automatic'), ('Manual', 'Manual')])
    # Add option to upload images
    image = models.ImageField(upload_to='vehicle_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} ({self.reg_no})"
    

# Optional: in models.py
def image_tag(self):
    if self.image:
        return format_html('<img src="{}" width="100" />'.format(self.image.url))
    return "No image"
image_tag.short_description = 'Image Preview'


class ServiceTicketModel(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('Yearly', 'Yearly'),
        ('Monthly', 'Monthly'),
        ('Quarterly', 'Quarterly'),
    ]


    STATUS_CHOICES = [
        ('Created', 'Created'),
        ('Estimation', 'Estimation'),
        ('Waiting for Customer approval', 'Waiting for Customer approval'),
        ('Customer Rejected', 'Customer Rejected'),
        ('Estimation Approved', 'Estimation Approved'),
        ('Checking with Customer', 'Checking with Customer'),
        ('Service in progress', 'Service in progress'),
        ('QA Check', 'QA Check'),
        ('Ready for delivery', 'Ready for delivery'),
        ('Customer query', 'Customer query'),
        ('Query resolved', 'Query resolved'),
        ('Waiting for payment', 'Waiting for payment'),
        ('Invoice Paid', 'Invoice Paid'),
        ('Waiting for Customer feedback', 'Waiting for Customer feedback'),
        ('Resolved', 'Resolved')]


    service_ticket_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    customer_mobile_number = models.CharField(max_length=15)
    customer_address = models.TextField()
    customer_email = models.EmailField()
    chassis_number = models.CharField(max_length=50)  # To fetch vehicle details
    reg_no = models.CharField(max_length=20, blank=True, null=True)
    make = models.CharField(max_length=50, blank=True, null=True)
    model = models.CharField(max_length=50, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    vin = models.CharField(max_length=17, blank=True, null=True)
    colour = models.CharField(max_length=50, blank=True, null=True)
    mileage = models.PositiveIntegerField(blank=True, null=True)
    trans = models.CharField(max_length=10, choices=[('Auto', 'Automatic'), ('Manual', 'Manual')], blank=True, null=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    service_advisor = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE, related_name='service_advisor_tickets')
    checkin_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE, related_name='created_tickets')
    complaints = models.TextField(blank=True, null=True)
    updated_by = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE, related_name='updated_tickets', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    image = models.ImageField(upload_to='uploads/images/', null=True, blank=True)
    document = models.FileField(upload_to='uploads/documents/', null=True, blank=True)
    video = models.FileField(upload_to='uploads/videos/', null=True, blank=True)    
    
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='')
    previous_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='')
    assigned_to = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE, related_name='assigned_tickets', blank=True, null=True)
    
    #history = models.ForeignKey('TicketTransitionHisotry', on_delete=models.CASCADE, related_name='ticket_history', blank=True, null=True)
    fuel_level = models.CharField(max_length=10, choices=[('E', 'Empty'), ('1/4', '1/4'), ('1/2', '1/2'), ('3/4', '3/4'), ('Full', 'Full')])
    spare_wheel = models.BooleanField(default=False)
    jack = models.BooleanField(default=False)
    tool_kit = models.BooleanField(default=False)
    any_warning_light_on = models.BooleanField(default=False)
    delivery_due_date = models.DateField(blank=True, null=True)

    # Optional: Add a field to track the vehicle's image
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    estimation_customer_confirmation = models.BooleanField(default=False)
    inspection_id = models.IntegerField(blank=True, null=True)
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    invoice_customer_confirmation = models.BooleanField(default=False)
    invoice_id = models.IntegerField(blank=True, null=True)
    customer_feedback_text = models.TextField(blank=True, null=True)
    customer_feedback_num = models.IntegerField(choices=[(1, 'Very Poor'), (2, 'Poor'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')], blank=True, null=True)
    history_log = models.TextField(blank=True, null=True, default="")
    inspection_notes = models.TextField(blank=True, null=True, default="NA")
  

    def save(self, *args, **kwargs):
        # Automatically populate vehicle details based on chassis_number
        if self.chassis_number:
            try:
                vehicle = VehicleModel.objects.get(chassis_number=self.chassis_number)
                self.reg_no = vehicle.reg_no
                self.make = vehicle.make
                self.model = vehicle.model
                self.year = vehicle.year
                self.vin = vehicle.vin
                self.colour = vehicle.colour
                self.mileage = vehicle.mileage
                self.trans = vehicle.trans
            except VehicleModel.DoesNotExist:
                pass  # Handle case where vehicle is not found
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Service Ticket {self.service_ticket_id} - {self.status}"


class InspectionModel(models.Model):
    
    service_ticket_id = models.IntegerField(default=0, blank=True, null=True)
    inspection_id = models.AutoField(primary_key=True)  # Optional: Use default `id` if not needed
    customer_name = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=50)
    vehicle_vin = models.CharField(max_length=50)
    inspection_notes = models.TextField()
    acceptance_notes = models.TextField(blank=True, null=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='uploads/inspections/', blank=True, null=True)
    class Meta:
        db_table = 'accounts_inspectionmodel'  # Adjust if different
    def __str__(self):
        return f"Inspection #{self.inspection_id} for Ticket #{self.service_ticket.service_ticket_id}"


class InvoiceModel(models.Model):
    service_ticket_id = models.IntegerField(default=0, blank=True, null=True)
    invoice_id = models.AutoField(primary_key=True)  # Optional: Use default `id` if not needed
    customer_name = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=50)
    vehicle_vin = models.CharField(max_length=50)
    invoice_amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_details = models.TextField(blank=True, null=True)
    customer_comments = models.TextField(blank=True, null=True)
    attachment = models.FileField(upload_to='uploads/invoices/', null=True, blank=True)

    class Meta:
        db_table = 'accounts_invoicemodel'  # Adjust if different

    def __str__(self):
        return f"Invoice #{self.invoice_id} for Ticket #{self.service_ticket.service_ticket_id}"


class CustomerFeedbackModel(models.Model):
    service_ticket = models.IntegerField(default=0, blank=True, null=True)
    inspection_id = models.AutoField(primary_key=True)  # Optional: Use default `id` if not needed
    customer_name = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=20)
    vehicle_model = models.CharField(max_length=50)
    vehicle_vin = models.CharField(max_length=50)
    # feedback from 1-5
    rating = models.IntegerField(choices=[(1, 'Very Poor'), (2, 'Poor'), (3, 'Average'), (4, 'Good'), (5, 'Excellent')])
    feeback_notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='uploads/feedbacks/', blank=True, null=True)

    class Meta:
        db_table = 'accounts_feedbackmodel'  # Adjust if different

    def __str__(self):
        return f"Inspection #{self.inspection_id} for Ticket #{self.service_ticket.service_ticket_id}"
