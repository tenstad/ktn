from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Section(models.Model):
    number = models.IntegerField()

    def __str__(self):
        return self.number


class Subsection(models.Model):
    section = models.ForeignKey(Section)
    number = models.IntegerField()

    def __str__(self):
        return '%r.%r' % (self.section, self.number)


class Question(models.Model):
    subsection = models.ForeignKey(Subsection)
    number = models.IntegerField()
    question = models.CharField(max_length=300)
    true = models.BooleanField(verbose_name='Answer')

    def __str__(self):
        return self.question if len(self.question) <= 30 else '%s...' % self.question[27:]


class Answer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    timestamp = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField()
