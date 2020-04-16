from django.urls import path
from . import views

urlpatterns = [
	path('', views.detection, name='home'),
	path('home/', views.detection, name='home'),
	path('about/', views.informations, name='about'),
]