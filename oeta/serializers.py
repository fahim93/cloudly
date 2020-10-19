from rest_framework import serializers
from .models import ExamPaper, Question, Student


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        # fields = '__all__'
        exclude = ['created_by', 'updated_by']


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        # fields = '__all__'
        exclude = ['user', 'created_by', 'updated_by']


class ExamPaperSerializer(serializers.HyperlinkedModelSerializer):
    questions = QuestionSerializer(read_only=True, many=True)
    students = StudentSerializer(read_only=True, many=True)

    class Meta:
        model = ExamPaper
        # fields = '__all__'
        exclude = ['created_by', 'updated_by']
