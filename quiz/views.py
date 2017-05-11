import random

from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View

from .models import Section, Subsection, Answer, Question as QuestionModel, Note


class Quiz(View):
    def get(self, request, *args, **kwargs):
        user = request.user

        context = {
            'sections': Section.objects.values_list('number', flat=True),
            'subsections': [a for a in range(1, 6)],
            'questions': [a for a in range(1, 11)],
        }

        def getnum(user_answers, question, user):
            answers = [a for a in user_answers if a[0] == question]
            if len(answers) == 0: return 0
            if len([a for a in answers if a[1] == True]): return 1
            return 2

        if user.is_authenticated:
            user_answers = Answer.objects.filter(user=user).values_list('question', 'correct')
            sections = Section.objects.values_list('number', flat=True)
            subsections = Subsection.objects.values_list('number', 'section__number')
            questions = QuestionModel.objects.values_list('id', 'number', 'subsection__number',
                                                          'subsection__section__number')

            tree = {}
            for section in sections:
                tree[section] = {}
            for subsection in subsections:
                tree[subsection[1]][subsection[0]] = []
            for question in questions:
                tree[question[3]][question[2]].append(question)

            total_list = []
            for section in sections:
                section_list = ([], section)
                for subsection in tree[section]:
                    subsection_list = ([], subsection)
                    for question in tree[section][subsection]:
                        subsection_list[0].append((getnum(user_answers, question[0], user),
                                                   '/quiz/%s/%s/%s/' % (section, subsection, question[1])))
                    section_list[0].append(subsection_list)
                total_list.append(section_list)

            context['list'] = total_list

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


class Notes(View):
    login_url = '/account/login/'

    def get(self, request, *args, **kwargs):
        context = {
            'notes': sorted(Note.objects.filter(user=request.user), key=lambda a: a.question.qid())
        }
        return render(request, 'quiz/notes.html', context)


class First(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(Section.objects.first().subsection_set.first().question_set.first().url())


class Last(View):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(Section.objects.last().subsection_set.last().question_set.last().url())


class Random(View):
    def get(self, request, *args, **kwargs):
        question_count = QuestionModel.objects.count()
        question = QuestionModel.objects.all()[random.randint(0, question_count - 1)]
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
            try:
                context['note'] = Note.objects.get(user=request.user, question=question).note
            except Note.DoesNotExist:
                pass

        return render(request, 'quiz/question.html', context)

    def post(self, request, section_num, subsection_num, question_num, *args, **kwargs):
        question = QuestionModel.get(section_num, subsection_num, question_num)
        if 'answer' in request.POST:
            correct = eval(request.POST['answer']) == question.true
            if request.user.is_authenticated:
                Answer.objects.create(question=question, user=request.user, correct=correct)
            return JsonResponse({
                'correct': correct,
            })
        elif 'note' in request.POST:
            if request.POST['note']:
                try:
                    note = Note.objects.get(user=request.user, question=question)
                except Note.DoesNotExist:
                    note = Note.objects.create(user=request.user, question=question)
                note.note = request.POST['note']
                note.save()
            else:
                return delete(request, section_num, subsection_num, question_num)

        return HttpResponseRedirect('/quiz/%s/%s/%s/' % (section_num, subsection_num, question_num))


def delete(request, section_num, subsection_num, question_num):
    question = QuestionModel.get(section_num, subsection_num, question_num)
    try:
        Note.objects.get(user=request.user, question=question).delete()
    except Note.DoesNotExist:
        pass
    return HttpResponseRedirect('/quiz/%s/%s/%s/' % (section_num, subsection_num, question_num))
