from django.forms import ModelForm
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import EmployeeModel, VehicleModel
from django.core.exceptions import ValidationError
from .models import ServiceTicketModel, InspectionModel, InvoiceModel, CustomerFeedbackModel
from .constants import ROLE_CHOICES

class login_form(AuthenticationForm):
    username = forms.CharField(label=_("Username"), max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'password']
        labels = {
            'username': _('Username'),
            'password': _('Password'),
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class resigistration_form(UserCreationForm):
    full_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = EmployeeModel
        fields = ['username', 'password1', 'password2', 'full_name', 'role', 'phone_number', 'address', 'date_of_birth', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    
    def clean_username(self):
        username = self.cleaned_data['username']
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            raise ValidationError(_("This username is already taken. Please choose another one."))
        return username



class edit_employee_profile_form(forms.ModelForm):
    class Meta:
        model = EmployeeModel
        exclude = ['username']  # Exclude username to prevent editing
        fields = ['full_name', 'role', 'phone_number', 'address', 'date_of_birth', 'profile_picture', 'email']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set fields to readonly

    def clean_email(self):
        email = self.cleaned_data['email']
        if EmployeeModel.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError(_("This email is already in use. Please choose another one."))
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        # Ensure read-only fields retain their initial values if not in POST
        for field in ['username']:
            if field not in cleaned_data or not cleaned_data[field]:
                cleaned_data[field] = self.initial.get(field)
        return cleaned_data

class vehicle_entry_form(forms.ModelForm):
    class Meta:
        model = VehicleModel
        fields = '__all__'
        widgets = {
            'delivery_due_date': forms.DateInput(attrs={'type': 'date'}),
            'check_in_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        # Ensure read-only fields retain their initial values if not in POST
        for field in ['vin', 'vehicle_id', 'reg_no', 'make', 'year', 'mileage', 'model', 'chassis_number', 'colour']:
            if field not in cleaned_data or not cleaned_data[field]:
                cleaned_data[field] = self.initial.get(field)
        return cleaned_data


class ServiceTicketForm(forms.ModelForm):
    class Meta:
        model = ServiceTicketModel
        fields = [
            'service_ticket_id', 'customer_name', 'customer_mobile_number', 'customer_address',
            'customer_email', 'chassis_number', 'reg_no', 'make', 'model', 'year',
            'vin', 'colour', 'mileage', 'trans', 'service_type', 'service_advisor', 'checkin_on',
            'created_by', 'complaints', 'updated_by', 'description', 'image', 'document', 'video', 'status', 'assigned_to',
            'fuel_level', 'spare_wheel', 'jack', 'tool_kit', 'any_warning_light_on',
            'delivery_due_date'
        ]
        labels = {
            'service_ticket_id': _('Service Ticket ID'),
            'customer_name': _('Customer Name'),
            'customer_mobile_number': _('Customer Mobile Number'),
            'customer_address': _('Customer Address'),
            'customer_email': _('Customer Email'),
            'chassis_number': _('Chassis Number'),
            'reg_no': _('Registration Number'),
            'make': _('Make'),
            'model': _('Model'),
            'year': _('Year'),
            'vin': _('VIN'),
            'colour': _('Colour'),
            'mileage': _('Mileage'),
            'trans': _('Transmission'),
            'service_type': _('Service Type'),
            'service_advisor': _('Service Advisor'),
            'checkin_on': _('Check-in On'),
            'created_by': _('Created By'),
            'complaints': _('Complaints'),
            'updated_by': _('Updated By'),
            'description': _('Description'),
            'image': _('Image'),
            'document': _('Document'),
            'video': _('Video'),            
            'status': _('Status'),
            'assigned_to': _('Assigned To'),
            'fuel_level': _('Fuel Level'),
            'spare_wheel': _('Spare Wheel'),
            'jack': _('Jack'),
            'tool_kit': _('Tool Kit'),
            'any_warning_light_on': _('Any Warning Light On'),
            'delivery_due_date': _('Delivery Due Date'),
        }
        widgets = {
            'service_ticket_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'chassis_number': forms.TextInput(attrs={'class': 'form-control'}),
            'reg_no': forms.TextInput(attrs={'class': 'form-control'}),
            'make': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'vin': forms.TextInput(attrs={'class': 'form-control'}),
            'colour': forms.TextInput(attrs={'class': 'form-control'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-control'}),
            'trans': forms.Select(attrs={'class': 'form-control'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'service_advisor': forms.Select(attrs={'class': 'form-control'}),
            'checkin_on': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'created_by': forms.Select(attrs={'class': 'form-control'}),
            'complaints': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'updated_by': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'fuel_level': forms.Select(attrs={'class': 'form-control'}),
            'spare_wheel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'jack': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tool_kit': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'any_warning_light_on': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'delivery_due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'document': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class InspectionForm(forms.ModelForm):
    class Meta:
        model = InspectionModel
        fields = ['service_ticket_id', 'customer_name', 'vehicle_number', 'vehicle_model', 'vehicle_vin', 'inspection_notes', 'estimated_cost', 'attachment']
        widgets = {
            'inspection_notes': forms.Textarea(attrs={'rows': 4}),
            'estimated_cost': forms.NumberInput(attrs={'min': 0}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set fields to readonly
        readonly_fields = ['service_ticket_id', 'customer_name', 'vehicle_number', 'vehicle_model', 'vehicle_vin']
        for field in readonly_fields:
            self.fields[field].widget.attrs['readonly'] = True
            self.fields[field].required = False  # Make fields non-required

    def clean(self):
        cleaned_data = super().clean()
        # Ensure read-only fields retain their initial values if not in POST
        for field in ['service_ticket_id', 'customer_name', 'vehicle_number', 'vehicle_model', 'vehicle_vin']:
            if field not in cleaned_data or not cleaned_data[field]:
                cleaned_data[field] = self.initial.get(field)
        return cleaned_data
    

class acceptance_form(forms.ModelForm):
    action = forms.ChoiceField(
        choices=[('accept', 'Accept'), ('reject', 'Reject')],
        widget=forms.RadioSelect,
        label="Action"
    )

    class Meta:
        model = InspectionModel
        fields = ['service_ticket_id', 'customer_name', 'vehicle_number', 'vehicle_model', 'vehicle_vin', 'inspection_notes', 'estimated_cost', 'acceptance_notes', 'action']
        widgets = {
            'service_ticket_id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'inspection_notes': forms.Textarea(attrs={'rows': 4, 'readonly': 'readonly'}),
            'estimated_cost': forms.NumberInput(attrs={'min': 0, 'readonly': 'readonly'}),
            'customer_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'vehicle_number': forms.TextInput(attrs={'readonly': 'readonly'}),
            'vehicle_model': forms.TextInput(attrs={'readonly': 'readonly'}),
            'vehicle_vin': forms.TextInput(attrs={'readonly': 'readonly'}),
            'acceptance_notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure all fields except 'action' are non-required since they are read-only
        for field in self.fields:
            if field != 'action':
                self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        # Ensure all fields have values from initial data
        for field in self.fields:
            if field != 'action' and not cleaned_data.get(field):
                cleaned_data[field] = self.initial.get(field)
                if not cleaned_data[field]:
                    raise forms.ValidationError(f"{field} cannot be empty.")
        if not cleaned_data.get('action'):
            raise forms.ValidationError("You must select an action (Accept or Reject).")
        return cleaned_data


class ticket_invoice_form(forms.ModelForm):
    class Meta:
        model = InvoiceModel
        fields = ['service_ticket_id', 'customer_name', 'vehicle_number', 'vehicle_model', 'vehicle_vin', 'invoice_details', 'invoice_amount', 'attachment']
        widgets = {
            'invoice_details': forms.Textarea(attrs={'rows': 4}),
            'invoice_amount': forms.NumberInput(attrs={'min': 0}),
            'attachment': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.png'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set fields to readonly
        readonly_fields = ['service_ticket_id', 'customer_name', 'vehicle_number', 'vehicle_model', 'vehicle_vin']
        for field in readonly_fields:
            self.fields[field].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        # Ensure read-only fields have valid, non-empty values
        required_fields = ['customer_name', 'vehicle_number', 'vehicle_model', 'vehicle_vin']
        for field in required_fields:
            value = cleaned_data.get(field) or self.initial.get(field)
            if not value:
                raise ValidationError(f"{field.replace('_', ' ').title()} is required and cannot be empty.")
            cleaned_data[field] = value
        # Handle service_ticket_id (optional, as it allows null)
        cleaned_data['service_ticket_id'] = cleaned_data.get('service_ticket_id') or self.initial.get('service_ticket_id')
        return cleaned_data

class ticket_invoice_confirmation_form(forms.ModelForm):
    class Meta:
        model = InvoiceModel
        fields = ['service_ticket_id', 'customer_name', 'vehicle_number', 'vehicle_model', 'vehicle_vin', 'invoice_details', 'invoice_amount', 'customer_comments']
        widgets = {
            'invoice_details': forms.Textarea(attrs={'rows': 4}),
            'customer_comments': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set fields to readonly
        readonly_fields = ['service_ticket_id', 'customer_name', 'vehicle_number', 'vehicle_model', 'vehicle_vin', 'invoice_details', 'invoice_amount']
        for field in readonly_fields:
            self.fields[field].widget.attrs['readonly'] = True
            self.fields[field].required = False  # Make fields non-required

    def clean(self):
        cleaned_data = super().clean()
        # Ensure read-only fields retain their initial values if not in POST
        for field in ['service_ticket_id', 'customer_name', 'vehicle_number', 'vehicle_model', 'vehicle_vin', 'invoice_details', 'invoice_amount', 'customer_comments']:
            if field not in cleaned_data or not cleaned_data[field]:
                cleaned_data[field] = self.initial.get(field)
        return cleaned_data



class customer_feedback_form(forms.ModelForm):
    class Meta:
        model = CustomerFeedbackModel
        fields = ['service_ticket', 'customer_name', 'vehicle_number', 'vehicle_model', 'vehicle_vin', 'rating', 'feeback_notes']
        widgets = {
            'invoice_details': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set fields to readonly
        readonly_fields = ['service_ticket', 'customer_name', 'vehicle_number', 'vehicle_model', 'vehicle_vin']
        for field in readonly_fields:
            self.fields[field].widget.attrs['readonly'] = True
            self.fields[field].required = False  # Make fields non-required

    def clean(self):
        cleaned_data = super().clean()
        # Ensure read-only fields retain their initial values if not in POST
        for field in ['service_ticket', 'customer_name', 'vehicle_number', 'vehicle_model', 'vehicle_vin', 'rating', 'feeback_notes']:
            if field not in cleaned_data or not cleaned_data[field]:
                cleaned_data[field] = self.initial.get(field)
        return cleaned_data


# Vehicles
class vehicle_entry_form(forms.ModelForm):
    class Meta:
        model = VehicleModel
        fields = '__all__'
        widgets = {
            'delivery_due_date': forms.DateInput(attrs={'type': 'date'}),
            'check_in_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
