from django.shortcuts import render
from django.views import View


class Quiz(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'quiz/quiz.html')