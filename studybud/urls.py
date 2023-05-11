from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # This line maps the URL / admin / to the
    # built-in administrative interface of the Django application
    # "" stand for root url,  This line maps the root URL (i.e., http://localhost:8000/) to the URL patterns defined in the base.urls module.
    path('', include('base.urls')),
]
