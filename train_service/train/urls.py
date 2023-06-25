from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_train_schedules, name='get_train_schedules'),
]
