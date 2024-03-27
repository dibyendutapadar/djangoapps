from django.urls import path
from . import views




urlpatterns =[
    path('',views.get_crossing,name='get_crossing'),
    path('get_directions/',views.get_directions,name='get_directions'),
    path('traffic_signal_simulation/',views.traffic_signal_simulation,name='traffic_signal_simulation')

]