from django.urls import path
from . import views

urlpatterns = [
    path('', views.createtimetable, name='createtimetable'),
    path('result/',views.resulttimetable, name='resulttimetable'),
]