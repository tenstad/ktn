from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Section(models.Model):
    number = models.IntegerField()

    class Meta:
        ordering = ['number']

    def __str__(self):
        return str(self.number)

    def next(self):
        try:
            return Section.objects.get(number=self.number + 1)
        except Section.DoesNotExist:
            return Section.objects.first()

    def previous(self):
        try:
            return Section.objects.get(number=self.number - 1)
        except Section.DoesNotExist:
            return Section.objects.last()


class Subsection(models.Model):
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING)
    number = models.IntegerField()

    class Meta:
        ordering = ['number']

    def __str__(self):
        return '%s.%s' % (self.section, str(self.number))

    def next(self):
        try:
            return Subsection.objects.get(section=self.section, number=self.number + 1)
        except Subsection.DoesNotExist:
            return self.section.next().subsection_set.first()

    def previous(self):
        try:
            return Subsection.objects.get(section=self.section, number=self.number - 1)
        except Subsection.DoesNotExist:
            return self.section.previous().subsection_set.last()


class Question(models.Model):
    subsection = models.ForeignKey(Subsection, on_delete=models.DO_NOTHING)
    number = models.IntegerField()
    question = models.CharField(max_length=300)
    true = models.BooleanField(verbose_name='Answer')

    class Meta:
        ordering = ['number']

    def __str__(self):
        return self.question

    def qid(self):
        return '%s.%s' % (self.subsection, self.number)

    def next(self):
        try:
            return Question.objects.get(subsection=self.subsection, number=self.number + 1)
        except Question.DoesNotExist:
            return self.subsection.next().question_set.first()

    def previous(self):
        try:
            return Question.objects.get(subsection=self.subsection, number=self.number - 1)
        except Question.DoesNotExist:
            return self.subsection.previous().question_set.last()

    def url(self):
        return '/quiz/%r/%r/%r/' % (self.subsection.section.number, self.subsection.number, self.number)

    @staticmethod
    def get(section_num, subsection_num, question_num):
        return Question.objects.get(number=question_num,
                                    subsection=Subsection.objects.get(number=subsection_num,
                                                                      section=Section.objects.get(number=section_num)))


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(default=timezone.now)
    correct = models.BooleanField(verbose_name='Answered correct')

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return '%s %r %s' % (self.user, self.correct, self.question)


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    note = models.CharField(max_length=500)

    def __str__(self):
        return self.note

    class Meta:
        ordering = ['-question']

    def lines(self):
        return self.note.split('\n')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=300)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return self.comment
