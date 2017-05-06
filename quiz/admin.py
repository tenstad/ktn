from django.contrib import admin

from .models import Section, Subsection, Question, Answer

admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(Question)
admin.site.register(Answer)
