# scrum/urls.py
from django.urls import path
from . import views

app_name ='scrum'
urlpatterns = [
    path('', views.start_scrum_call, name='start_scrum_call'),
    path('update/', views.update_sprint_status, name='update_sprint_status'),
    path('analytics/', views.show_analytics, name='show_analytics'),
    path('retrospective/', views.show_retrospective, name='show_retrospective'),
    path('end/', views.end_scrum_call, name='end_scrum_call'),
    path('times/', views.show_scrum_call_times, name='show_scrum_call_times'),
]