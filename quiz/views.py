from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View

from .models import Section, Answer, Question as QuestionModel


class Quiz(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'quiz/quiz.html')


class Continue(View):
    def get(self, request, *args, **kwargs):
        try:
            return HttpResponseRedirect(Answer.objects.filter(user=request.user).last().question.next().url())
        except AttributeError:
            return HttpResponseRedirect(Section.objects.first().subsection_set.first().question_set.first().url())


class Question(View):
    def get(self, request, section_num, subsection_num, question_num, *args, **kwargs):
        question = QuestionModel.get(section_num, subsection_num, question_num)
        results = [a.correct for a in Answer.objects.filter(question=question, user=request.user).order_by('timestamp')]
        context = {
            'question': question,
            'results': results,
        }
        return render(request, 'quiz/question.html', context)

    def post(self, request, section_num, subsection_num, question_num, *args, **kwargs):
        question = QuestionModel.get(section_num, subsection_num, question_num)
        correct = eval(request.POST['answer']) == question.true
        Answer.objects.create(question=question, user=request.user, correct=correct)
        return JsonResponse({
            'correct': correct,
        })