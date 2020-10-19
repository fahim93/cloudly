from django.http import HttpResponse
from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework import viewsets

from .serializers import ExamPaperSerializer, QuestionSerializer, StudentSerializer

from .models import ExamPaper, Question, Student


# Create your views here.


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('title')
    serializer_class = QuestionSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ExamPaperViewSet(viewsets.ModelViewSet):
    queryset = ExamPaper.objects.all().order_by('title')
    serializer_class = ExamPaperSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('students__email',)
