from django.conf import settings
from django.db import models

# Create your models here.
from smart_selects.db_fields import ChainedManyToManyField

from users.models import User


class Subject(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'subjects'
        verbose_name_plural = 'subjects'.title()
        ordering = ('title',)


class Question(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, related_name='questions')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'questions'
        verbose_name_plural = 'questions'.title()
        ordering = ('title',)
        unique_together = ('title', 'subject')


class Choice(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='choices')
    is_correct = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'choices'
        verbose_name_plural = 'choices'.title()
        ordering = ('title',)
        unique_together = ('title', 'question')


class ExamPaper(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    questions = ChainedManyToManyField(
        Question,
        horizontal=True,
        verbose_name='questions',
        chained_field="subject",
        chained_model_field="subject")
    is_published = models.BooleanField(default=False)
    students = models.ManyToManyField('Student', blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'exam_papers'
        verbose_name_plural = 'exam papers'.title()
        ordering = ('title',)
        unique_together = ('title', 'subject')


class ExamPaperSet(models.Model):
    exam_paper = models.ForeignKey('ExamPaper', on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, blank=True, null=True)
    set = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        return "Set %s" % self.set

    class Meta:
        db_table = 'exam_paper_sets'
        verbose_name_plural = 'exam paper sets'.title()
        ordering = ('exam_paper',)
        # unique_together = ('exam_paper', 'question', 'set')


class Student(User):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="+")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        db_table = 'students'
        verbose_name_plural = 'students'.title()
        ordering = ('email',)




