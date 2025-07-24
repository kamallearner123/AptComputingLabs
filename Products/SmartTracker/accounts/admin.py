from django.contrib import admin
from accounts.models import EmployeeModel, VehicleModel, ServiceTicketModel

# Register your models here.
admin.site.register(EmployeeModel)
admin.site.register(VehicleModel)
admin.site.register(ServiceTicketModel)
admin.site.site_header = "Smart Tracker Admin"
admin.site.site_title = "Smart Tracker Admin Portal"
admin.site.index_title = "Welcome to Smart Tracker Admin Portal"
admin.site.site_url = "https://www.smarttracker.com"
