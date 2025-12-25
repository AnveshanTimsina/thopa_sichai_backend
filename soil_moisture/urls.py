from django.urls import path
from . import views

app_name = 'soil_moisture'

urlpatterns = [
    path('soil-moisture/', views.list_soil_moisture, name='list-soil-moisture'),
    path('soil-moisture/create/', views.create_soil_moisture, name='create-soil-moisture'),
    path('soil-moisture/receive/', views.receive_soil_moisture, name='receive-soil-moisture'),
    path('soil-moisture/latest/', views.latest_soil_moisture, name='latest-soil-moisture'),
    path('soil-moisture/<uuid:pk>/update/', views.update_soil_moisture, name='update-soil-moisture'),
    path('soil-moisture/<uuid:pk>/delete/', views.delete_soil_moisture, name='delete-soil-moisture'),
]

