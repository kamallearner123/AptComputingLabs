from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('core.urls')),
    path('judge/', include('judge.urls')),
    path('', RedirectView.as_view(url='/', permanent=False)),
]
