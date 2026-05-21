from django.urls import path
from . import views

app_name = 'iot'

urlpatterns = [
    path('soil-moisture/', views.list_iot, name='list-soil-moisture'),
    path('soil-moisture/create/', views.create_iot, name='create-soil-moisture'),
    path('soil-moisture/receive/', views.receive_iot, name='receive-soil-moisture'),
    path('soil-moisture/latest/', views.latest_iot, name='latest-soil-moisture'),
    path('soil-moisture/<uuid:pk>/update/', views.update_iot, name='update-soil-moisture'),
    path('soil-moisture/<uuid:pk>/delete/', views.delete_iot, name='delete-soil-moisture'),
]

