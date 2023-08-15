from django.urls import path
from . import views

urlpatterns = [
	path('contact-list/', views.EmployeeContactList, name="emp-contact-list"),
		
]