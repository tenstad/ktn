from django.conf.urls import url

from .views import Login, Register, Logout, Account

urlpatterns = [
    url(r'^$', Account.as_view(), name='account'),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^logout/$', Logout.as_view(), name='logout'),
]