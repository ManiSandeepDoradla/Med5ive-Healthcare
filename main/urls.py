from django.urls import path
from . import views
urlpatterns=[
    path('',views.main,name='main'),
    path('profile_page',views.profile_page,name='profile_page'),
    path('filter',views.filter,name='filter'),
    path('filter1',views.filter1,name='filter1'),
    path('filter2',views.filter2,name='filter2'),
    path('my_appointments',views.my_appointments,name='my_appointments'),
    path('book_appointment_step1',views.book_appointment_step1,name='book_appointment_step1'),
    path('confirm_appointment',views.confirm_appointment,name='confirm_appointment'),
]