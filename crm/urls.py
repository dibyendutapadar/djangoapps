from django.urls import path
from . import views




urlpatterns =[
    path('admin/',views.admin_home,name='admin_home'),
    path('admin/contact',views.admin_contact,name='admin_contact'),
    path('admin/contact/add', views.add_contact, name='add_contact'),
    path('custom/contact/add', views.custom_add_contact_view, name='custom_add_contact'),

]