import random

from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View

from .models import Section, Subsection, Answer, Question as QuestionModel


class Quiz(View):
    def get(self, request, *args, **kwargs):
        context = {
            'sections': [section.number for section in Section.objects.all()],
            'subsections': [a for a in range(1, 6)],
            'questions': [a for a in range(1, 11)],
        }

        def getnum(user_answers, question, user):
            answers = user_answers.filter(question=question)
            if answers.count() == 0: return 0
            if answers.filter(correct=True).exists(): return 1
            return 2

        if request.user.is_authenticated:
            user = request.user
            user_answers = Answer.objects.filter(user=user)
            context['list'] = [([([(getnum(user_answers, question, user), question.url()) for question in subsection.question_set.all()], subsection.number) for subsection in section.subsection_set.all()], section.number) for section in Section.objects.all()]

        return render(request, 'quiz/quiz.html', context)

    def post(self, request, *args, **kwargs):
        try:
            section = request.POST['section']
            subsection = request.POST['subsection']
            question = request.POST['question']

            if not section:
                section = Section.objects.first()
            else:
                section = Section.objects.get(number=section)
            if not subsection:
                subsection = section.subsection_set.first()
            else:
                subsection = Subsection.objects.get(section=section, number=subsection)
            if not question:
                question = subsection.question_set.first()
            else:
                question = QuestionModel.objects.get(subsection=subsection, number=question)

            return HttpResponseRedirect('/quiz/%s/%s/%s/' % (section.number, subsection.number, question.number))
        except (ValueError, Section.DoesNotExist, Subsection.DoesNotExist, QuestionModel.DoesNotExist):
            messages.error(request, 'Spørsmålet eksisterer ikke')
            return HttpResponseRedirect('/quiz/')


class First(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(Section.objects.first().subsection_set.first().question_set.first().url())


class Last(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(Section.objects.last().subsection_set.last().question_set.last().url())


class Random(View):
    def get(self, request, *args, **kwargs):
        question_count = QuestionModel.objects.count()
        question = QuestionModel.objects.all()[random.randint(0, question_count-1)]
        return HttpResponseRedirect(question.url())


class Continue(View):
    def get(self, request, *args, **kwargs):
        try:
            return HttpResponseRedirect(Answer.objects.filter(user=request.user).last().question.url())
        except (AttributeError, TypeError):
            return HttpResponseRedirect(Section.objects.first().subsection_set.first().question_set.first().url())


class Question(View):
    def get(self, request, section_num, subsection_num, question_num, *args, **kwargs):
        question = QuestionModel.get(section_num, subsection_num, question_num)
        context = {
            'question': question,
        }
        if request.user.is_authenticated:
            answers = Answer.objects.filter(question=question, user=request.user)
            if answers.exists():
                if answers.filter(correct=True).exists():
                    context.update({'result': 1})
                else:
                    context.update({'result': 2})

        return render(request, 'quiz/question.html', context)

    def post(self, request, section_num, subsection_num, question_num, *args, **kwargs):
        question = QuestionModel.get(section_num, subsection_num, question_num)
        correct = eval(request.POST['answer']) == question.true
        if request.user.is_authenticated:
            Answer.objects.create(question=question, user=request.user, correct=correct)
        return JsonResponse({
            'correct': correct,
        })
