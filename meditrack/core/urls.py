from django.urls import path
from .views import dashboard_view, medications
urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('medications/', medications, name="medications")
  ]