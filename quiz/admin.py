from django.contrib import admin

from .models import Section, Subsection, Question, Answer


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'correct', 'correct_answer', 'qid', 'question')
    search_fields = ('question__question', 'user__username')

    def qid(self, object):
        return object.question.qid()

    def correct_answer(self, object):
        return object.question.true

    correct_answer.boolean = True


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('qid', 'true', 'question')
    search_fields = ('question',)


admin.site.register(Answer, AnswerAdmin)
admin.site.register(Question, QuestionAdmin)

admin.site.register(Section)
admin.site.register(Subsection)
