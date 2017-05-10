from django.conf.urls import url
from .views import Quiz, Question, Continue, First, Last, Random, delete

urlpatterns = [
    url(r'^$', Quiz.as_view()),
    url(r'^continue', Continue.as_view()),
    url(r'^first', First.as_view()),
    url(r'^last', Last.as_view()),
    url(r'^random', Random.as_view()),
    url(r'^(?P<section_num>[0-9]+)/(?P<subsection_num>[0-9]+)/(?P<question_num>[0-9]+)/deletenote/', delete),
    url(r'^(?P<section_num>[0-9]+)/(?P<subsection_num>[0-9]+)/(?P<question_num>[0-9]+)/$', Question.as_view()),
]
