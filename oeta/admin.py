from django.contrib import admin

# Register your models here.
from oeta.models import Subject, Question, Choice, ExamPaper


class ChoiceInline(admin.TabularInline):
    model = Choice
    fields = ['title', 'is_correct']
    extra = 4
    max_num = 5


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Subject._meta.fields]
    list_display_links = ['title']
    exclude = ('created_by', 'updated_by')
    search_fields = ('title',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject']
    list_display_links = ['title']
    exclude = ('created_by', 'updated_by')
    search_fields = ('title',)
    autocomplete_fields = ('subject',)
    list_filter = ['subject__title']
    inlines = [ChoiceInline]


# @admin.register(Choice)
# class ChoiceAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Choice._meta.fields]
#     list_display_links = ['title']
#     exclude = ('created_by', 'updated_by')
#     autocomplete_fields = ('question',)


@admin.register(ExamPaper)
class ExamPaperAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject']
    list_display_links = ['title']
    exclude = ('created_by', 'updated_by')