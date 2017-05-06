from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Section(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return str(self.number)


class Subsection(models.Model):
    section = models.ForeignKey(Section)
    number = models.IntegerField()

    def __str__(self):
        return '%s.%s' % (self.section, str(self.number))


class Question(models.Model):
    subsection = models.ForeignKey(Subsection)
    number = models.IntegerField()
    question = models.CharField(max_length=300)
    true = models.BooleanField(verbose_name='Answer')

    def __str__(self):
        return self.question

    def qid(self):
        return '%s.%s' % (self.subsection, self.number)


class Answer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    timestamp = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(verbose_name='Answered correct')

    def __str__(self):
        return '%s %r %s' % (self.user, self.correct, self.question)