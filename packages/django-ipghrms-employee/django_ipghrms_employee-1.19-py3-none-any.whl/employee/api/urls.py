from django.urls import path
from . import views

urlpatterns = [
	path('gender/', views.APIGender.as_view(), name="emp-api-gender"),
	path('nivelaca/', views.APINivelAca.as_view(), name="emp-api-nivelaca"),
	path('unit/', views.APIUnit.as_view(), name="emp-api-unit"),
	path('dep/', views.APIDep.as_view(), name="emp-api-dep"),
	path('u/dep/', views.uAPIDep.as_view(), name="u-emp-api-dep"),
	path('mun/', views.APIMun.as_view(), name="emp-api-mun"),
	path('country/', views.APICountry.as_view(), name="emp-api-country"),
	path('age/', views.APIAge.as_view(), name="emp-api-age"),
	path('all/', views.APIAllStaff.as_view(), name="emp-api-all"),
]