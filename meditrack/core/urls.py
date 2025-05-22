from django.urls import path
from .views import dashboard_view, medications, user_account, add_reminder
urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('medications/', medications, name="medications"),
    path('user_account/', user_account, name="user_account"),
    path('add_reminder/', add_reminder, name="add_reminder")
  ]