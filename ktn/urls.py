from django.conf.urls import url, include
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Index.as_view()),
    url(r'^account/', include('account.urls')),
    url(r'^quiz/', include('quiz.urls')),
]
