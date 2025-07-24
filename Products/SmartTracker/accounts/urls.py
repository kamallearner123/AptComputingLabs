from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from .views import register_view, login_view, dashboard_view
from .views import create_ticket_view, view_all_tickets_view
from .views import ticket_details_view, view_my_tickets_view
from .views import get_vehicle_details_view, ticket_edit_view, ticket_inspection_view
from .views import get_ticket_details, ticket_acceptance_view
from .views import ticket_acceptance_view
from .views import display_employee_profile_view
from .views import edit_employee_profile_view
from .views import ticket_invoice_view, ticket_customer_feedback_confirm_view, ticket_customer_feedback_view
from .views import ticket_invoice_confirmation_view, user_logout
from django.conf import settings
from django.conf.urls.static import static


# Temporary view to show all URLs are in progress
def in_progress_view(request):
    return HttpResponse("All URLs are currently in progress.")

def home_page(request):
    return render(request, 'home.html', {'user': request})

def dummy_edit_ticket_view(request, ticket_id):
    return HttpResponse(f"Edit ticket id {ticket_id} view is in progress.")

def dummy_employee_tickets_view(request):
    return HttpResponse("Employee tickets view is in progress.")

def dummy_create_ticket_view(request):
    return HttpResponse("Create ticket view is in progress.")



urlpatterns = [
    path('', home_page, name='home_page'),
    
    # User authentication URLs
    path('home/', home_page, name='home'),
    path('signup/', register_view, name='signup'),
    path('register/', register_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', user_logout, name='logout'),

    # Profiles and Dashboard URLs
    path('dashboard/',dashboard_view, name='dashboard'),
    path('view-employee-profile/', display_employee_profile_view, name='view-employee-profile'),
    path('edit-employee-profile/', edit_employee_profile_view, name='edit-employee-profile'),

    # Tickets and Vehicle URLs
    path('create-ticket/', create_ticket_view, name='create_ticket'),
    path('view_all_tickets/', view_all_tickets_view, name='view_all_tickets'),
    path('ticket_details/<int:ticket_id>/', ticket_details_view, name='ticket_details'),
    path('view_my_tickets/', view_my_tickets_view, name='view_my_tickets'),
    path('edit_ticket/<int:ticket_id>/', ticket_edit_view, name='edit_ticket'),
    path('get_ticket_details/<str:ticket_id>/', get_ticket_details, name='get_ticket_details'),
    path('ticket_inspection/<int:ticket_id>/', ticket_inspection_view, name='ticket_inspection'),
    path('ticket_acceptance/<str:token>/', ticket_acceptance_view, name='ticket_acceptance'),
    path('ticket_invoice/<int:ticket_id>/', ticket_invoice_view, name='ticket_invoice'),
    path('ticket_invoice_confirmation/<str:token>/', ticket_invoice_confirmation_view, name='ticket_invoice_confirmation'),
    path('ticket_customer_feedback/<int:ticket_id>/', ticket_customer_feedback_view, name='ticket_customer_feedback'),
    path('ticket_customer_feedback_confirm/<str:token>/', ticket_customer_feedback_confirm_view, name='ticket_customer_feedback_confirm'),

    # Vehicle URLs
    path('get_vehicle_details/<str:chassis_number>/', get_vehicle_details_view, name='get_vehicle_details'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# This enables serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)