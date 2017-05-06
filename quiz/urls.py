from django.conf.urls import url, include
from .views import Quiz, Question, Continue

urlpatterns = [
    url(r'^$', Quiz.as_view()),
    url(r'^continue', Continue.as_view()),
    url(r'(?P<section_num>[0-9]+)/(?P<subsection_num>[0-9]+)/(?P<question_num>[0-9]+)/', Question.as_view()),
]
