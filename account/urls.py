from django.urls import path

from .views import Login, Register, Logout, Account

urlpatterns = [
    path('', Account.as_view(), name='account'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
]
