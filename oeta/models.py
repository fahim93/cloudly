from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from smart_selects.db_fields import ChainedManyToManyField


class Subject(models.Model):
    title = models.CharField(max_length=255, unique=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')

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
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')

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
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')

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
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'exam_papers'
        verbose_name_plural = 'exam_papers'.title()
        ordering = ('title',)
        unique_together = ('title', 'subject')


