from django.urls import path
from .views import Quiz, Question, Continue, First, Last, Random, Notes, delete

urlpatterns = [
    path('', Quiz.as_view()),
    path('continue/', Continue.as_view()),
    path('first/', First.as_view()),
    path('last/', Last.as_view()),
    path('random/', Random.as_view()),
    path('notes/', Notes.as_view()),
    path('<int:section_num>/<int:subsection_num>/<int:question_num>/deletenote/', delete),
    path('<int:section_num>/<int:subsection_num>/<int:question_num>/', Question.as_view()),
]
