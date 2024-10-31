from django.urls import path
from .views import get_users, login_request

urlpatterns = [
    path('login/', login_request,name='login_request'),
    path('user/', get_users,name='get_users'),
]