from django.urls import path
from . import views

urlpatterns = [
	path('academic/level/list/', views.RAcaLevelList, name="r-emp-acalevel-list"),
]