from django.urls import path
from . import views



app_name ='food'
urlpatterns =[
    path('',views.index,name='index'),
    path('items',views.items,name='items'),
    path('<int:item_id>/',views.item_detail,name='item_detail')
]