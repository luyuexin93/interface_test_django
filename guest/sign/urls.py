from django.contrib import admin
from django.urls import path,re_path,include
from django.conf.urls import url
from sign import views_if
from sign import views_if_sec

app_name='sign'
urlpatterns = [
    path('add_event/', views_if.add_event,name='add_event'),
    path('get_event_list/',views_if.get_event_list,name='get_event_list'),
    path('add_guest/',views_if.add_guest,name='add_guest'),
    path('get_guest_list/',views_if.get_guest_list,name='get_guest_list'),
    path('user_sign/',views_if.user_sign,name='user_sign'),
    path('sec_get_event_list/',views_if_sec.get_event_list,name="sec_get_event_list"),
    path('sec_add_event/',views_if_sec.add_event,name="sec_add_event")

]