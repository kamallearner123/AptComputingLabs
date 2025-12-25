from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date')

from .models import SessionPhoto


@admin.register(SessionPhoto)
class SessionPhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'taken_at')
