from django.urls import path
from .views import dashboard_view, medications, user_account, add_reminder, manage_medications, edit_medication, delete_medication
urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('medications/', medications, name="medications"),
    path('user_account/', user_account, name="user_account"),
    path('add_reminder/', add_reminder, name="add_reminder"),
    path('manage_medications', manage_medications, name="manage_medications"), 
    path('edit_medication/<int:medication_id>/', edit_medication, name='edit_medication'),
    path('delete_medication/<int:medication_id>/', delete_medication, name='delete_medication')
  ]