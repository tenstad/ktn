from django.urls import path, include
from django.contrib import admin
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view()),
    path('account/', include('account.urls')),
    path('quiz/', include('quiz.urls')),
]
