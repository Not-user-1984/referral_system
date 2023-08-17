from django.urls import path
from . import views

urlpatterns = [
    path('api/request_phone_number/',
         views.request_phone_number,
         name='request_phone_number'),
    path('api/verify_code/', views.verify_code, name='verify_code'),
    path('api/activate_invite_code/',
         views.activate_invite_code,
         name='activate_invite_code'),
    path('api/invited-users/',
         views.invited_users_list,
         name='invited-users-list'),
    path('api/user_profile/',
         views.user_profile,
         name='user_profile'),
]
