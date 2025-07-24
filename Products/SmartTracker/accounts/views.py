from django.shortcuts import render
from .forms import login_form
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import resigistration_form, vehicle_entry_form
from .models import EmployeeModel, VehicleModel, InvoiceModel
from .models import ServiceTicketModel, InspectionModel, CustomUserProfile
from .forms import ServiceTicketForm, InspectionForm, acceptance_form, customer_feedback_form
from .forms import ticket_invoice_confirmation_form
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseNotFound
from django.core.signing import TimestampSigner
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.core.signing import BadSignature
from django.http import HttpResponse
from .forms import ticket_invoice_form
from .constants import Event
from django.contrib.auth import logout
from datetime import datetime
from .forms import edit_employee_profile_form
import re
from django.core.mail import EmailMessage

# Define a function to check if the status change is valid
def is_valid_status_change(ticket, new_status):
    # Define valid transitions
    valid_transitions = {
        'Created': ['Estimation'],
        'Estimation': ['Waiting for Customer approval'],
        'Waiting for Customer approval': ['Customer Rejected', 'Estimation Approved'],
        'Estimation Approved': ['Service in progress'],
        'Customer Rejected': ['Checking with Customer'],
        'Checking with Customer': ['Customer query'],
        'Service in progress': ['QA Check'],
        'QA Check': ['Ready for delivery'],
        'Ready for delivery': ['Waiting for payment'],
        'Waiting for payment': ['Invoice Paid', 'Customer query'],
        'Invoice Paid': [],
        'Waiting for Customer feedback': ['Resolved']
    }
    return new_status in valid_transitions.get(ticket.status, [])


def service_ticket_status_change(ticket, event):
    return_value = True
    history_log = f"Ticket ID: {ticket.service_ticket_id}, Status: {ticket.status}, Event: {event}"
    if (ticket.status == '' or ticket.status == 'Created') and event == Event.CREATED:
        ticket.status = 'Created'
    elif ticket.status == 'Created' and event == Event.ESTIMATION:
        ticket.status = 'Estimation'
    elif ticket.status == 'Estimation' and event == Event.SENT_ESTIMATION:
        ticket.status = 'Waiting for Customer approval'
    elif ticket.status == 'Waiting for Customer approval' and event == Event.RECEIVED_CONFORMATION_ON_ESTIMATION:
        ticket.status = 'Estimation Approved'
    elif ticket.status == 'Estimation Approved' and event == Event.START_WORK:
        ticket.status = 'Service in progress'
    elif ticket.status == 'Waiting for Customer approval' and event == Event.RECEIVED_REJECTION_ON_ESTIMATION:
        ticket.status = 'Customer Rejected'
    elif ticket.status == 'Customer Rejected' and event == Event.CLEARED_CUSTOMER_QUERY:
        ticket.status = 'Checking with Customer'
    elif ticket.status == 'Checking with Customer' and event == Event.RECEIVED_CHANGE_IN_ESTIMATION:
        ticket.status = 'Customer query'
    elif ticket.status == 'Customer query' and event == Event.CHECKING_WITH_CUSTOMER:
        ticket.status = 'Service in progress'
    elif ticket.status == 'Service in progress' and event == Event.WORK_FINISHED:
        ticket.status = 'Ready for delivery'
    elif ticket.status == 'Ready for delivery' and event == Event.SENT_INVOICE:
        ticket.status = 'Waiting for payment'
    elif ticket.status == 'Waiting for payment' and event == Event.RECEIVED_PAYMENT:
        ticket.status = 'Invoice Paid'
    elif ticket.status == 'Waiting for payment' and event == Event.RECEIVED_PAYMENT_REJECTION:
        ticket.status = 'Customer query'
    elif ticket.status == 'Invoice Paid' and event == Event.DELIVERED:
        ticket.status = 'Waiting for Customer feedback'
    elif ticket.status == 'Waiting for Customer feedback' and event == Event.RECEIVED_CUSTOMER_FEEDBACK:
        ticket.status = 'Resolved'
    elif event == Event.UNKNOWN:
        if ticket.previous_status != ticket.status:
            ticket.previous_status = ticket.status  
        else:
            print("No status change required.")
            return True
    else:
        return False
    ticket.previous_status = ticket.status  # Store the previous status
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ticket.history_log = (ticket.history_log or "") + f", New Status: {ticket.status} on {current_date} assigned to {ticket.assigned_to};"
    ticket.save()
    return return_value

def send_email_to_customer(ticket, subject, message):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[ticket.customer_email],
    )

def user_logout(request):
    logout(request)
    return redirect('accounts:home')  # Redirect to login page after logout

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = login_form(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accounts:dashboard')  # Or your desired post-login page
    else:
        form = login_form(request=request)  # ✅ Fix applied here
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = resigistration_form(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Automatically log the user in after registration
            login(request, user)
            return redirect('accounts:dashboard')  # Redirect to dashboard after registration
    else:
        form = resigistration_form()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def dashboard_view(request):
    try:
        # My Tickets (user-specific, created by the user)
        my_tickets = ServiceTicketModel.objects.filter(created_by=request.user)
        my_total_tickets = my_tickets.count()
        # Active: Any status except 'Resolved', 'Customer Rejected', or 'Invoice Paid'
        my_active_tickets = my_tickets.exclude(status__in=['Resolved']).count()
        # Resolved: Only 'Resolved' status (or 'Invoice Paid' if considered resolved)
        my_resolved_tickets = my_tickets.filter(status='Resolved').count()

        # All Tickets (system-wide)
        all_tickets = ServiceTicketModel.objects.all()
        all_total_tickets = all_tickets.count()
        all_active_tickets = all_tickets.exclude(status__in=['Resolved']).count()
        all_resolved_tickets = all_tickets.filter(status='Resolved').count()

        # Recent Tickets (up to 5, most recent first, based on checkin_on)
        recent_tickets = my_tickets.order_by('-checkin_on')[:5]

        context = {
            'my_total_tickets': my_total_tickets,
            'my_active_tickets': my_active_tickets,
            'my_resolved_tickets': my_resolved_tickets,
            'all_total_tickets': all_total_tickets,
            'all_active_tickets': all_active_tickets,
            'all_resolved_tickets': all_resolved_tickets,
            'recent_tickets': recent_tickets,
        }
        print(f"Dashboard context for user {request.user.username}: {context}")
    except Exception as e:
        print(f"Error in dashboard view for user {request.user.username}: {str(e)}")
        context = {
            'my_total_tickets': 0,
            'my_active_tickets': 0,
            'my_resolved_tickets': 0,
            'all_total_tickets': 0,
            'all_active_tickets': 0,
            'all_resolved_tickets': 0,
            'recent_tickets': [],
        }

    return render(request, 'DashBoards/employee_dashboard.html', context)

@login_required
def employee_tickets_view(request):
    if request.user.is_authenticated:
        return render(request, 'DashBoards/view_all_tickets.html')
    else:
        return redirect('accounts:login')

    
# Vehicles
@login_required
def vehicle_entry(request):
    if request.method == 'POST':
        form = vehicle_entry_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('vehicles/vehicle_detail.html')  # Define your own success page
    else:
        form = vehicle_entry_form()
    return render(request, 'vehicles/vehicle_form.html', {'form': form})

# Service Tickets
@login_required
def create_ticket_view(request):
    print("CSRF TOKEN:", get_token(request)) 
    if request.method == 'POST':
        form = ServiceTicketForm(request.POST)
        if form.is_valid():
            print("Form is valid")  # Debugging line
            # Save the form but do not commit to the database yet
            ticket = form.save(commit=False)

            # Set the user who created the ticket
            ticket.created_by = request.user

            # Print ticket details for debugging
            print("Ticket details:", ticket)

            ticket.status = 'Created'  # Set initial status
            service_ticket_status_change(ticket, Event.CREATED)

            # Commit the ticket to the database
            ticket.save()
            return redirect('accounts:view_all_tickets')  # update this to your success view
        else:
            print("Form errors:", form.errors)
            # Print form errors for debugging
            print("Form is not valid")
            for field, errors in form.errors.items():
                print(f"Field: {field}, Errors: {errors}")
    else:
        form = ServiceTicketForm()
        form.initial['created_by'] = request.user  # Set the initial value for created_by
        if request.user.is_authenticated:
            form.initial['assigned_to'] = request.user
            form.initial['status'] = 'Created'
            form.initial['created_by'] = request.user
            form.initial['updated_by'] = request.user
            Employee = EmployeeModel.objects.get(username=request.user.username)
            if Employee.role == 'Service Advisor':
                form.initial['Service Advisor'] = request.user
    print(f"******** ticket form ***************")
    return render(request, 'tickets/ticket_form.html', {'form': form})

@login_required
def view_my_tickets_view(request):
    if request.user.is_authenticated:
        try:
            employee = EmployeeModel.objects.get(username=request.user.username)
            tickets = ServiceTicketModel.objects.filter(assigned_to=employee)
            print("Tickets for user:", tickets)
            return render(request, 'tickets/view_all_tickets.html', {'tickets': tickets})
        except EmployeeModel.DoesNotExist:
            print("EmployeeModel does not exist for user:", request.user.username)
            return render(request, 'tickets/view_all_tickets.html', {'tickets': []})
    else:
        return redirect('accounts:login')

@login_required
def view_all_tickets_view(request):
    if request.user.is_authenticated:
        tickets = ServiceTicketModel.objects.all()
        return render(request, 'tickets/view_all_tickets.html', {'tickets': tickets})
    else:
        return redirect('accounts:login')

@login_required
def ticket_edit_view(request, ticket_id):
    ticket = get_object_or_404(ServiceTicketModel, pk=ticket_id)
    
    if request.method == 'POST':
        form = ServiceTicketForm(request.POST, instance=ticket)
        
        if form.is_valid():
            form.save()
            
            # Access cleaned_data after form is valid
            status_value = form.cleaned_data.get("status")
            service_ticket_id = form.cleaned_data.get("service_ticket_id")  # or form.instance.service_ticket_id
            
            service_ticket_status_change(ticket, Event.UNKNOWN)

            # Pass these to the template
            context = {
                "form": form,
                "status_value": status_value,
                "service_ticket_id": service_ticket_id,
            }
            return redirect('accounts:ticket_details', ticket_id=ticket_id)
    else:
        form = ServiceTicketForm(instance=ticket)
        
        # Access initial data or other attributes directly if needed
        status_value = form.initial.get("status")
        service_ticket_id = form.instance.service_ticket_id
        
        # Pass these values to the template
        context = {
            "form": form,
            "status_value": status_value,
            "service_ticket_id": service_ticket_id,
        }
    
    return render(request, 'tickets/ticket_form.html', context)


def extract_statuses(status_string):
    # Regex to capture: status text + full datetime + assigned_to
    pattern = r"New Status:\s+(.+?)\s+on\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+assigned to\s+(.+?);"
    matches = re.findall(pattern, status_string)

    # Create a list of dictionaries with 'date', 'status', and 'assigned_to'
    statuses = [{"date": match[1], "status": match[0].strip(), "assigned_to": match[2].strip()} for match in matches]
    return statuses

@login_required
def ticket_details_view(request, ticket_id):
    list_of_statuses = extract_statuses(ServiceTicketModel.objects.get(service_ticket_id=ticket_id).history_log)
    
    if request.user.is_authenticated:
        try:
            ticket = ServiceTicketModel.objects.get(service_ticket_id=ticket_id)
            print("Ticket fetched:", ticket)  # Debugging line
            print("List of statuses:", list_of_statuses)  # Debugging line
            return render(request, 'tickets/ticket_details.html', {'ticket': ticket, 'list_of_statuses': list_of_statuses})
        except ServiceTicketModel.DoesNotExist:
            print("Ticket does not exist for ID:", ticket_id)  # Debugging line
            return redirect('accounts:view_all_tickets')
    else:
        return redirect('accounts:login')

def get_customer_details(phone_number):
    print("Phone number received:", phone_number)  # Debugging line
    try:
        customer = CustomUserProfile.objects.get(phone_number=phone_number)
        data = {
            'customer_name': f"{customer.user.first_name} {customer.user.last_name}",
            'customer_mobile_number': customer.phone_number or '',
            'customer_address': customer.address or '',
            'customer_email': customer.user.email or '',
        }
        print("Customer data:", data)  # Debugging line
        return data
    except CustomUserProfile.DoesNotExist:
        print("Customer does not exist for phone number:", phone_number)  # Debugging line
        return {
            'customer_name': '',
            'customer_mobile_number': '',
            'customer_address': '',
            'customer_email': '',
        }

def get_vehicle_details_view(request, chassis_number):
    print("Chassis number received:", chassis_number)  # Debugging line
    try:
        vehicle = VehicleModel.objects.get(chassis_number=chassis_number)
        data = {
            'vin': vehicle.vin or '',
            'reg_no': vehicle.reg_no or '',
            'make': vehicle.make or '',
            'model': vehicle.model or '',
            'year': vehicle.year or '',
            'colour': vehicle.colour or '',
            'mileage': vehicle.mileage or '',
            'trans': vehicle.trans or '',
        }

        # Get customer details if customer_id exists and is valid
        customer_details = {
            'customer_name': '',
            'customer_mobile_number': '',
            'customer_address': '',
            'customer_email': '',
        }
        if vehicle.customer_id_id:  # Check if customer_id is not None
            try:
                # Use user_id to fetch CustomUserProfile
                customer_profile = CustomUserProfile.objects.get(user_id=vehicle.customer_id_id)
                customer_details = get_customer_details(customer_profile.phone_number)
            except CustomUserProfile.DoesNotExist:
                print("Invalid customer_id for vehicle:", chassis_number)
            except AttributeError:
                print("Customer phone_number is missing for vehicle:", chassis_number)
        else:
            print("No customer_id associated with vehicle:", chassis_number)

        data.update(customer_details)

        print("Vehicle and customer data:", data)  # Debugging line
        return JsonResponse(data)
    except VehicleModel.DoesNotExist:
        print("Vehicle does not exist for chassis number:", chassis_number)  # Debugging line
        return JsonResponse({'error': 'Vehicle not found'}, status=404)


# Write get_ticket_details function
def get_ticket_details(request, ticket_id):
    print("Ticket ID received:", ticket_id)  # Debugging line
    try:
        ticket = ServiceTicketModel.objects.get(service_ticket_id=ticket_id)
        data = {
            'customer_name': ticket.customer_name,
            'customer_mobile_number': ticket.customer_mobile_number,
            'customer_address': ticket.customer_address,
            'customer_email': ticket.customer_email,
            'chassis_number': ticket.chassis_number,
            'reg_no': ticket.reg_no,
            'make': ticket.make,
            'model': ticket.model,
            'year': ticket.year,
            'vin': ticket.vin,
            'colour': ticket.colour,
            'mileage': ticket.mileage,}
        print("Ticket data:", data)  # Debugging line
        return JsonResponse(data)
    except ServiceTicketModel.DoesNotExist:
        print("Ticket does not exist for ID:", ticket_id)
        return JsonResponse({}, status=404)


@login_required
def ticket_inspection_view(request, ticket_id):
    ticket = get_object_or_404(ServiceTicketModel, pk=ticket_id)

    if request.method == 'POST':

        form = InspectionForm(request.POST)
        if form.is_valid():
            # Save the form but do not commit to the database yet
            inspection = form.save(commit=False)
            inspection.service_ticket_id = ticket.service_ticket_id  # Ensure service_ticket is set
            # inspection.customer_name = ticket.customer_name  # Preserve read-only fields
            # inspection.vehicle_number = ticket.reg_no
            # inspection.vehicle_model = ticket.model
            # inspection.vehicle_vin = ticket.vin
            inspection.inspection_notes = form.cleaned_data['inspection_notes']
            inspection.estimated_cost = form.cleaned_data['estimated_cost']
            inspection.technician = request.user  # if applicable

            inspection.save()
            print("ticket_inspection_view: In Inspection: ", inspection.__dict__)  # Debugging line

            ticket.acceptance_id = inspection.inspection_id  # Link the inspection id to the ticket
            ticket.estimated_cost = inspection.estimated_cost
            ticket.inspection_notes = inspection.inspection_notes
            ticket.inspection_id = inspection.inspection_id
            ticket.save()

            signer = TimestampSigner()
            token = signer.sign(str(inspection.inspection_id))  # Convert ticket_id to string
            url = reverse('accounts:ticket_acceptance', args=[token])

            # Send email to customer with attachment

            email = EmailMessage(
                subject="Car Service: Service Estimate for approval for your vehicle: Ticket ID: " + str(ticket.service_ticket_id),
                body=(
                    f"Hello {form.cleaned_data['customer_name']},\n\n"
                    f"We've completed the inspection of your vehicle and prepared an estimate for the service.\n"
                    f"Estimated Cost: ${form.cleaned_data['estimated_cost']}\n\n"
                    f"To proceed, please review and accept the estimate using the link below:\n"
                    f"http://127.0.0.1:8000{url}\n\n"
                    f"If you have any questions or need further clarification, feel free to reply to this email.\n\n"
                    f"Thank you,\n"
                    f"Smart Tracker Service Team"
                ),
                from_email="kamalbec2004@gmail.com",
                to=[ticket.customer_email],
            )

            # Attach a file (e.g., PDF invoice)
            print("#######################################")
            print("Debugging request.FILES", request.FILES)
            print("#######################################")
            if 'attachment' in request.FILES:
                estimations_file = request.FILES['attachment']
                email.attach(estimations_file.name, estimations_file.read(), estimations_file.content_type)

            email.send()

            messages.success(request, "Estimation sent to customer.")

            if service_ticket_status_change(ticket, Event.SENT_ESTIMATION) != True:
                print("Invalid status for estimation.")
            

            return redirect('accounts:ticket_details', ticket_id=ticket_id)
    else:
        initial_data = {
            'service_ticket': ticket,
            'customer_name': ticket.customer_name,
            'vehicle_number': ticket.reg_no,
            'vehicle_model': ticket.model,
            'vehicle_vin': ticket.vin,
            'service_ticket_id': ticket.service_ticket_id,
        }        
        form = InspectionForm(initial=initial_data)

    return render(request, 'tickets/inspection_form.html', {
        'form': form,
        'ticket': ticket
    })


def ticket_acceptance_view(request, token):
    # Create a signer to verify the token
    signer = TimestampSigner()

    try:
        # Decode the token to get the inspection ID
        inspection_id = signer.unsign(token, max_age=86400)  # max_age is 24 hours
    except BadSignature:
        return redirect('error_page')  # Redirect to a page with an error message

    # Fetch the inspection record
    inspection = get_object_or_404(InspectionModel, inspection_id=inspection_id)

    # Get the associated service ticket
    ticket = get_object_or_404(ServiceTicketModel, service_ticket_id=inspection.service_ticket_id)

    if request.method == 'POST':
        print("**********************************************")
        print("Accptance View:request: ",request)  # Debugging line
        print("**********************************************")        
        form = acceptance_form(request.POST)
        if form.is_valid():
            print("**********************************************")
            print("Accptance View: form is valid: ",form)  # Debugging line
            print("**********************************************")

            action = request.POST.get("action")

            if action == "accept":
                ticket.estimation_customer_confirmation = True
                print(" Ticket info")
                print("Ticket ID:", ticket.service_ticket_id)
                print(f"********Status {ticket.status} ***************")
                if not service_ticket_status_change(ticket, Event.RECEIVED_CONFORMATION_ON_ESTIMATION):
                    return HttpResponse("Invalid status for acceptance.")
                print(f"********Status {ticket.status} ***************")

            elif action == "reject":
                ticket.estimation_customer_confirmation = False
                if not service_ticket_status_change(ticket, Event.RECEIVED_REJECTION_ON_ESTIMATION):
                    return HttpResponse("Invalid status for rejection.")
            else:
                return HttpResponse("Invalid action. Please choose Accept or Reject.")

            # Update the ticket status and save
            ticket.estimated_cost = inspection.estimated_cost
            ticket.save()

            # Send a confirmation email to the customer
            send_mail(
                subject="Car Service: Estimate Status",
                message=(
                    f"Dear {ticket.customer_name},\n\n"
                    f"Your estimation response has been processed. Current status: {ticket.status}.\n\n"
                    f"Details:\n"
                    f"- Customer: {inspection.customer_name}\n"
                    f"- Vehicle Number: {inspection.vehicle_number}\n"
                    f"- Vehicle Model: {inspection.vehicle_model}\n"
                    f"- Vehicle VIN: {inspection.vehicle_vin}\n"
                    f"- Inspection Notes: {inspection.inspection_notes}\n"
                    f"- Estimated Cost: ${inspection.estimated_cost}\n\n"
                    f"Thank you for your response.\n"
                ),
                from_email="kamalbec2004@gmail.com",
                recipient_list=[ticket.customer_email],
            )

            return HttpResponse("Thank you for your response.")
        else:
            print("Form errors:", form.errors)
            return HttpResponse("Form is not valid.")
    else:
        # Pre-fill the form with inspection details
        initial_data = {
            'service_ticket_id': ticket.service_ticket_id,
            'customer_name': inspection.customer_name,
            'vehicle_number': inspection.vehicle_number,
            'vehicle_model': inspection.vehicle_model,
            'vehicle_vin': inspection.vehicle_vin,
            'inspection_notes': inspection.inspection_notes,
            'estimated_cost': inspection.estimated_cost,
        }
        form = acceptance_form(initial=initial_data)

    return render(request, 'tickets/acceptance_form.html', {'form': form, 'ticket': ticket})


@login_required
def ticket_invoice_view(request, ticket_id):
    ticket = get_object_or_404(ServiceTicketModel, pk=ticket_id) 
    if request.method == 'POST':
        form = ticket_invoice_form(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.service_ticket_id = ticket.service_ticket_id
            ticket.invoice_id = invoice.invoice_id
            print("ticket_invoice_view: In Invoice: ", invoice.__dict__)  # Debugging line
            invoice.save()

            signer = TimestampSigner()
            token = signer.sign(str(invoice.invoice_id))  # Convert invoice_id to string
            url = reverse('accounts:ticket_invoice_confirmation', args=[token])

            # Send email to customer
            email = EmailMessage(
                subject="Car Service: Service Invoice for your vehicle: Ticket ID: " + str(ticket.service_ticket_id),
                body=(
                    f"Hello {form.cleaned_data['customer_name']},\n\n"
                    f"We've completed the service of your vehicle and prepared an invoice.\n"
                    f"Please review the invoice details in attachement.\n"
                    f"Invoice Amount: ${form.cleaned_data['invoice_amount']}\n\n"
                    f"To proceed, please review and accept the invoice using the link below:\n"
                    f"http://127.0.0.1:8000{url}\n\n"
                    f"If you have any questions or need further clarification, feel free to reply to this email.\n\n"
                    f"Thank you,\n"
                    f"Smart Tracker Service Team"
                ),
                from_email="kamalbec2004@gmail.com",
                to=[ticket.customer_email],
            )

            # Attach a file (e.g., PDF invoice)
            print("#######################################")
            print("Debugging request.FILES", request.FILES)
            print("#######################################")
            if 'attachment' in request.FILES:
                invoice_file = request.FILES['attachment']
                email.attach(invoice_file.name, invoice_file.read(), invoice_file.content_type)

            email.send()
            messages.success(request, "Invoice sent to customer.")
            if service_ticket_status_change(ticket, Event.SENT_INVOICE) != True:
                print("Invalid status for invoice.")
            ticket.save()

            return redirect('accounts:ticket_details', ticket_id=ticket_id)
    else:
        initial_data = {
            'service_ticket_id': ticket.service_ticket_id,
            'customer_name': ticket.customer_name,
            'vehicle_number': ticket.reg_no,
            'vehicle_model': ticket.model,
            'vehicle_vin': ticket.vin,
        }
        form = ticket_invoice_form(initial=initial_data)
    return render(request, 'tickets/invoice_form.html', {
        'form': form,
        'ticket': ticket
    })


# Uncomment this function if you want to use it

# @login_required
def ticket_invoice_confirmation_view(request, token):
    # Create a signer to verify the token
    signer = TimestampSigner()

    # Validate the token
    # Decode the token to get the ticket ID
    try:
        # Decode the token to get the ticket ID
        invoice_id = signer.unsign(token, max_age=86400)  # max_age is 24 hours
        print("Decoded invoice ID:", invoice_id)  # Debugging line
        print("Decoded token:", token)  # Debugging line
    except BadSignature:
        # If the token is invalid or expired, return an error
        return redirect('error_page')  # Redirect to a page with an error message

    # Invoice object from invoice_id
    invoice = get_object_or_404(InvoiceModel, pk=invoice_id)    

    if request.method == 'POST':

        print("Responce from customer: ", request.POST)  # Debugging line
        # Handle the form submission (accept or reject)
        form = ticket_invoice_confirmation_form(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.save()

            ticket = get_object_or_404(ServiceTicketModel, pk=invoice.service_ticket_id)

            # Send a confirmation email to the user
            send_mail(
                subject="Car Service: Invoice Letter",
                message=f"Dear {ticket.customer_name}, your estimate has been {ticket.status}.",
                from_email="kamalbec2004@gmail.com",
                recipient_list=[ticket.customer_email],
            )

            action = request.POST.get("action")

            if action == "accept":
                if service_ticket_status_change(ticket, Event.RECEIVED_PAYMENT) != True:
                    print("Invalid status for invoice confirmation.")

                ticket.invoice_id = invoice.invoice_id
                ticket.invoice_amount = invoice.invoice_amount
                ticket.invoice_details = invoice.invoice_details
                ticket.invoice_confirmation = True
                ticket.save()
            elif action == "reject":
                if service_ticket_status_change(ticket, Event.RECEIVED_PAYMENT_REJECTION) != True:
                    print("Invalid status for invoice rejection.")
                ticket.invoice_confirmation = False
                ticket.save()
            else:
                return HttpResponse("Invalid action. Please choose Accept or Reject.")

            return HttpResponse("Thank you for your response.")
    else:
        # If it's a GET request, pre-fill the form with the ticket details
        initial_data = {
            'service_ticket_id': invoice.service_ticket_id,
            'customer_name': invoice.customer_name,
            'vehicle_number': invoice.vehicle_number,
            'vehicle_model': invoice.vehicle_model,
            'vehicle_vin': invoice.vehicle_vin,
            'invoice_amount': invoice.invoice_amount,
            'invoice_details':invoice.invoice_details,
        }
        form = ticket_invoice_confirmation_form(initial=initial_data)
        ticket = get_object_or_404(ServiceTicketModel, pk=invoice.service_ticket_id)

    return render(request, 'tickets/ticket_invoice_confirm.html', {'form': form, 'ticket': ticket})


@login_required
def ticket_customer_feedback_view(request, ticket_id):
    # Get service ticket object
    ticket = get_object_or_404(ServiceTicketModel, pk=ticket_id)
    # Make an url for configuring the acceptance
    signer = TimestampSigner()
    token = signer.sign(str(ticket_id))  # Convert ticket_id to string
    url = reverse('accounts:ticket_customer_feedback_confirm', args=[token])
    # Send email to customer
    send_mail(
        subject="Car Service:Customer Feedback",
        message=(
            f"Hello {ticket.customer_name},\n\n"
            f"We would like to hear your feedback on our service.\n"
            f"Please click the link below to provide your feedback:\n"
            f"http://127.0.0.1:8000{url}\n\n"
            f"If you have any questions or need further clarification, feel free to reply to this email.\n\n"
            f"Thank you,\n"
            f"Smart Tracker Service Team"
        ),
        from_email="kamalbec2004@gmail.com",
        recipient_list=[ticket.customer_email],

    )
    messages.success(request, "Feedback request sent to customer.")

    if service_ticket_status_change(ticket, Event.DELIVERED) != True:
        print("Invalid status for customer feedback.")
    ticket.save()
    return redirect('accounts:ticket_details', ticket_id=ticket_id)


def ticket_customer_feedback_confirm_view(request, token):
    # Create a signer to verify the token
    signer = TimestampSigner()
    # Validate the token
    # Decode the token to get the ticket ID
    try:
        # Decode the token to get the ticket ID
        ticket_id = signer.unsign(token, max_age=86400)  # max_age is 24 hours
        print("Decoded ticket ID:", ticket_id)  # Debugging line
        print("Decoded token:", token)  # Debugging line
    except BadSignature:
        # If the token is invalid or expired, return an error
        return redirect('error_page')
    # Fetch the ticket record
    ticket = get_object_or_404(ServiceTicketModel, pk=ticket_id)
    # Get the associated service ticket
    if request.method == 'POST':
        print("Responce from customer: ", request.POST)
        # Handle the form submission (accept or reject)
        form = customer_feedback_form(request.POST)
        if form.is_valid():
            confirmation = form.save(commit=False)

            ticket.customer_feedback_text = confirmation.feeback_notes
            ticket.customer_feedback_num = confirmation.rating
            if service_ticket_status_change(ticket, Event.RECEIVED_CUSTOMER_FEEDBACK) != True:
                print("Invalid status for customer feedback.")
            
            # Send a confirmation email to the user
            send_mail(
                subject="Car Service: Customer Feedback",
                message=f"Dear {ticket.customer_name}, your feedback has been received.",
                from_email="kamalbec2004@gmail.com",
                recipient_list=[ticket.customer_email],
            )
            return HttpResponse("Thank you for your response.")
    else:
        # If it's a GET request, pre-fill the form with the ticket details
        initial_data = {
            'service_ticket': ticket.service_ticket_id,
            'customer_name': ticket.customer_name,
            'vehicle_number': ticket.reg_no,
            'vehicle_model': ticket.model,
            'vehicle_vin': ticket.vin,
        }
        form = customer_feedback_form(initial=initial_data)
    return render(request, 'tickets/customer_feedback_form.html', {'form': form, 'ticket': ticket})

@login_required
def display_employee_profile_view(request):
    if request.user.is_authenticated:
        try:
            employee = EmployeeModel.objects.get(username=request.user.username)
            return render(request, 'DashBoards/view_employee_profile.html', {'employee': employee})
        except EmployeeModel.DoesNotExist:
            return HttpResponseNotFound("Employee not found.")
    else:
        return redirect('accounts:login')
    
@login_required
def edit_employee_profile_view(request):
    try:
        employee = EmployeeModel.objects.get(username=request.user.username)
        if request.method == 'POST':
            form = edit_employee_profile_form(request.POST, request.FILES, instance=employee)
            if form.is_valid():
                form.save()
                return redirect('accounts:view-employee-profile')
        else:
            form = edit_employee_profile_form(instance=employee)
        return render(request, 'DashBoards/edit_employee_profile.html', {'form': form})
    except EmployeeModel.DoesNotExist:
        return HttpResponseNotFound("Employee not found.")
